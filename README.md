# KMD Nova Password Bot

This robot is meant to run on [OpenOrchestrator](https://github.com/itk-dev-rpa/OpenOrchestrator).
The purpose of this robot is to change passwords for KMD Nova accounts.

## Setup

Process parameters is required, setup as a comma-seperated string:
"Robot 123", "KMD robot".

## Requirements

Minimum python version 3.10

## Linting and Github Actions

This template is also setup with flake8 and pylint linting in Github Actions.
This workflow will trigger whenever you push your code to Github.
The workflow is defined under `.github/workflows/Linting.yml`.

