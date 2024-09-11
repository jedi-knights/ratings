#!/usr/bin/env zsh

# Organizations
# Organization(id=22, season_id=67, name='BOYS PRE-ECNL', season_group_id=9)
# Organization(id=12, season_id=61, name='ECNL Boys', season_group_id=9)
# Organization(id=16, season_id=63, name='ECNL Boys Regional League', season_group_id=9)
# Organization(id=9, season_id=60, name='ECNL Girls', season_group_id=9)
# Organization(id=13, season_id=62, name='ECNL Girls Regional League', season_group_id=9)
# Organization(id=21, season_id=66, name='GIRLS PRE-ECNL', season_group_id=9)

# Supported Years: 07, 08, 09, 10

# Read ECNL Girls Matches
python3 driver.py matches --gender girls --year 07 --organization-id 9
python3 driver.py matches --gender girls --year 08 --organization-id 9
python3 driver.py matches --gender girls --year 09 --organization-id 9
python3 driver.py matches --gender girls --year 10 --organization-id 9

# Read ECNL Boys Matches
python3 driver.py matches --gender boys --year 07 --organization-id 12
python3 driver.py matches --gender boys --year 08 --organization-id 12
python3 driver.py matches --gender boys --year 09 --organization-id 12
python3 driver.py matches --gender boys --year 10 --organization-id 12

# Read ECRL Girls Matches
python3 driver.py matches --gender girls --year 07 --organization-id 13
python3 driver.py matches --gender girls --year 08 --organization-id 13
python3 driver.py matches --gender girls --year 09 --organization-id 13
python3 driver.py matches --gender girls --year 10 --organization-id 13

# Read ECRL Boys Matches
python3 driver.py matches --gender boys --year 07 --organization-id 16
python3 driver.py matches --gender boys --year 08 --organization-id 16
python3 driver.py matches --gender boys --year 09 --organization-id 16
python3 driver.py matches --gender boys --year 10 --organization-id 16


# Calculate Statistics for ECNL Girls
python3 driver.py stats -f matches_girls_07_ecnl.csv --organization-id 9
python3 driver.py stats -f matches_girls_08_ecnl.csv --organization-id 9
python3 driver.py stats -f matches_girls_09_ecnl.csv --organization-id 9
python3 driver.py stats -f matches_girls_10_ecnl.csv --organization-id 9

# Calculate Statistics for ECRL Girls
python3 driver.py stats -f matches_girls_07_ecrl.csv --organization-id 13
python3 driver.py stats -f matches_girls_08_ecrl.csv --organization-id 13
python3 driver.py stats -f matches_girls_09_ecrl.csv --organization-id 13
python3 driver.py stats -f matches_girls_10_ecrl.csv --organization-id 13

# Calculate Statistics for ECNL Boys
python3 driver.py stats -f matches_boys_07_ecnl.csv --organization-id 12
python3 driver.py stats -f matches_boys_08_ecnl.csv --organization-id 12
python3 driver.py stats -f matches_boys_09_ecnl.csv --organization-id 12
python3 driver.py stats -f matches_boys_10_ecnl.csv --organization-id 12

# Calculate Statistics for ECRL Boys
python3 driver.py stats -f matches_boys_07_ecrl.csv --organization-id 16
python3 driver.py stats -f matches_boys_08_ecrl.csv --organization-id 16
python3 driver.py stats -f matches_boys_09_ecrl.csv --organization-id 16
python3 driver.py stats -f matches_boys_10_ecrl.csv --organization-id 16
