#!/usr/bin/env bash

py.test --postgres="${TEST_POSTGRES_STORAGE}" \
        --cov-config=.coveragerc --cov=moneyhand \
         -x -vvv tests/
