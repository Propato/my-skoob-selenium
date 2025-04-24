#!/bin/bash

run_single_test(){
    clear
    while true; do
        read -p  "Test Name (<tests/users/test_UserExample.py>) or C (Close): " filename
        if [[ $filename = "C" || $filename = "c" ]]; then
            echo ""
            echo "Closing..."
            break
        fi
        if [[ -f "$ROOT_DIRECTORY/$filename" ]]; then
            while true; do
                print_highlight "Running $1/$filename" 1 0
                sudo docker exec -it $TEST_CONTAINER pytest -vv ./$filename
                echo ""
                print_highlight "Test Finished" 0 1

                select OPTIONS3 in \
                    "Run again" \
                    "Back to Menu"; do
                case $OPTIONS3 in
                    "Run again")
                        break
                        ;;
                    "Back to Menu")
                        echo ""
                        echo "Closing..."
                        return
                        ;;
                esac
                done
            done
        else
            echo ""
            echo "Test not Found: '$ROOT_DIRECTORY/$filename'"
        fi
    done
    clear
}

check_containers() {
    if [[ -z $(sudo docker container ls -qf NAME=$TEST_CONTAINER) || \
          -z $(sudo docker container ls -qf NAME=$HUB_CONTAINER) || \
          -z $(sudo docker container ls -qf NAME=chrome-1) || \
          -z $(sudo docker container ls -qf NAME=chrome-2) || \
          -z $(sudo docker container ls -qf NAME=chrome-3) || \
          -z $(sudo docker container ls -qf NAME=$FRONT_CONTAINER) || \
          -z $(sudo docker container ls -qf NAME=$BACK_CONTAINER) || \
          -z $(sudo docker container ls -qf NAME=$DB_CONTAINER)
        ]]; then
        echo ""
        echo "Local Environment not Started."
        return 1
    else
        return 0
    fi
}

print_highlight(){
    width=$(tput cols)
    line=$(printf '%*s' "$width" '' | tr ' ' '=')
    padding=$(( (width - ${#1}) / 2 ))

    if [[ $2 = 1 ]]; then echo "$line"
    fi

    echo "$(printf '%*s%s%*s' "$padding" '' "$1" "$padding" '')"

    if [[ $3 = 1 ]]; then echo "$line"
    fi

    echo ""
}

clean_reports(){
    cd "$ROOT_DIRECTORY/reports"
    > ./report.txt
    rm -f *.xml

    cd "$ROOT_DIRECTORY/prints"
    rm -f *.png */*.png

    cd "$ROOT_DIRECTORY"
}

clear
COLUMNS=20
cd "$(pwd)"
ROOT_DIRECTORY="$(pwd)"
SKOOB_DIRECTORY="$(pwd)/my-skoob"
FRONT_DIRECTORY="$SKOOB_DIRECTORY/my-skoob-frontend"
BACK_DIRECTORY="$SKOOB_DIRECTORY/my-skoob-backend"

WORKERS=6
RERUN=2

TEST_CONTAINER=myTester
HUB_CONTAINER=selenium-hub
FRONT_CONTAINER=skoob-frontend
BACK_CONTAINER=skoob-backend
DB_CONTAINER=skoob-psql

PS3=$'\n Select Option: '
select OPTIONS in \
    "Start Local Environment" \
    "Run Single Test" \
    "Run All Tests" \
    "Delete Data" \
    "Delete Containers" \
    "Delete Local Environment" \
    "Close"; do

case $OPTIONS in
    "Start Local Environment")
        clear

        git pull origin main
        git submodule update --init --recursive
        cd $SKOOB_DIRECTORY
        git pull origin main
        cd $ROOT_DIRECTORY
        git submodule update --init --recursive

        sudo docker compose up -d --build
        echo ""

        echo "Local Environment Ready!"
        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Run Single Test")
        clear

        if check_containers; then
            run_single_test
        fi

        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Run All Tests")
        clear

        if check_containers; then
            clean_reports

            print_highlight "Running All Tests" 1 1

            sudo docker exec -it $TEST_CONTAINER pytest -v -n $WORKERS --ignore=tests/baseClasses --reruns $RERUN --junitxml=reports/all-report.xml -o junit_logging=all tests/

            print_highlight "Tests Completed" 1 1
            echo ""
        fi

        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Delete Data")
        clear

        sudo rm -rf $BACK_DIRECTORY/data/postgres/data

        echo ""
        echo "Data deleted."
        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Delete Containers")
        clear

        sudo docker compose down

        echo ""
        echo "Containers and Volumes Deleted."
        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Delete Local Environment")
        clear

        sudo docker compose down --rmi 'all'
        sudo rm -rf $BACK_DIRECTORY/data/postgres/data
        clean_reports

        echo ""
        echo "Environment Deleted."
        read -p "[Press Enter to Close]"
        clear
        COLUMNS=1
        ;;

    "Close")
        clear
        break
        COLUMNS=1
        ;;
esac
done