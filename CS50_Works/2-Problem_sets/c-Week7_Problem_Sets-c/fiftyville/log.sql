-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = 'Humphrey Street';
--The Theft happen at 10:15 am at the Humphrey Street bakery three witnesses at the time
SELECT transcript FROM interviews WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';
--The three witnesses have three evidence the First one is "In 10 min of the theft the theif got into car then exit the security footage would catch him lefting the parking in that time frame

SELECT name FROM people
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = 'exit';
--The first witness Suspects : Vanessa , Bruce , Barry , Luca , Sofia , Iman , Diana , Kelsey

--The Second witness The theif earlier the day of theft the theif withdrawing money from ATM at "Leggett Street"
SELECT name FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw';
--The second witness Suspects : Bruce , Diana , Brooke , Kenny , Iman , Luca , Taylor , Benista
--The common Suspects : Bruce , Luca , Iman , Diana

--The third witness "The theif after leaving the bakery called in phone with someone in less than minute the theif plan to take the earliest flight out of Fiftyville tomorrow the theif ask the person on the other end to purshase the flight tikcket
SELECT name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE passengers.flight_id IN  (
    SELECT id FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (
        SELECT id FROM airports WHERE city = 'Fiftyville')
    ORDER BY hour,minute
    LIMIT 1);
--The third witness suspects : Doris , Sofia , Bruce , Edward , Kelsey , Taylor , Kenny , Luca
--The common Suspects : Bruce , Luca

--The Forth Evidence the call that less than one minute
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE year = 2021 AND month = 7 AND day = 28 AND duration <=60;
--The Forth Evidence Suspects :Sofia , Kelsey , Bruce , Kathryn , Kelsey , Taylor , Diana , Carina , Kenny , Benista
--The common Suspects : Bruce
--The theif is Bruce

--Getting the city that the theif traveled to
SELECT city FROM airports
JOIN flights ON airports.id = flights.destination_airport_id
WHERE year = 2021 AND month = 7 AND day = 29 AND flights.id = (
    SELECT flight_id FROM passengers
    JOIN people ON passengers.passport_number = people.passport_number
    WHERE people.name = 'Bruce'
);
--The city where the theif is travel to is 'New York City'

--Getting the person that the theif talked to
SELECT name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE year = 2021 AND month = 7 AND day = 28 AND duration <=60 AND phone_calls.caller = (
    SELECT phone_number FROM people WHERE name = 'Bruce'
);
--The name of the one who helped the theif is 'Robin'

-- The name of the theif , city traveled , who helped the theif  is 'Bruce' , 'New York City' , 'Robin'