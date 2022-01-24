<?php

ini_set('display_errors', '1');
error_reporting(E_ALL);

$DB_FILE = '/home/mbirth/opt/garmin-fetch/spo2.db3';   // path to SQLite database
$DAYS_BACK = 1;   // Today minus $DAYS_BACK days

$pdo = new \PDO('sqlite:' . $DB_FILE);

$now = gmmktime(0, 0, 0);   // get today at 00:00:00 according to UTC/GMT
$servefrom = $now - $DAYS_BACK * 24 * 60 * 60;
#$servefrom = 1643001299;

$pq = $pdo->prepare('SELECT * FROM spo2 WHERE timestamp_utc >= ?');
$pq->execute(array($servefrom));
$res = $pq->fetchAll();

#header('Content-Type: text/plain');
header('Content-Type: application/json');

$result = array();
foreach ($res as $row) {
    $dto = new DateTime('@' . $row['timestamp_utc'], new DateTimeZone('UTC'));
    $result[] = array(
        'unixtime' => intval($row['timestamp_utc']),
        #'datestr' => $dto->format('Y.m.d \A\D \a\t H:i:s \U\T\C'),
        'datestr' => $dto->format('c'),
        'spo2_value' => intval($row['spo2_percent']),
        'spo2_confidence' => intval($row['spo2_confidence']),
    );
}

#var_dump($result);
echo json_encode($result);
