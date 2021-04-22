/*SELECT*/
SELECT audio_file_id
FROM KEYWORDS
WHERE  = 'immigrants' = ANY(keyword);

SELECT title, date_published, audio_file_id, description 
FROM AUDIO_FILE
WHERE audio_file_id = 'JHS10SideA';

SELECT interviewer_id 
FROM INTERVIEWER
WHERE name = 'Jake Survey';

SELECT audio_file_id
FROM INTERVIEWED_BY
WHERE interviewer_id IN (1);

SELECT title, date_published, audio_file_id, description 
FROM AUDIO_FILE
WHERE audio_file_id IN ('JHS50SideA');

SELECT interviewee_id
FROM INTERVIEWEE
WHERE name = 'Samuel Rudner';

SELECT audio_file_id
FROM INTERVIEW_OF
WHERE interviewee_id IN (2,3);

SELECT title, date_published, audio_file_id, description 
FROM AUDIO_FILE
WHERE audio_file_id IN ('JHS50SideA','JHS55SideA');

SELECT interviewee_id
FROM INTERVIEWEE_RACES
WHERE race = 'white';

SELECT audio_file_id 
FROM INTERVIEW_OF
WHERE interviewee_id in (1,3);

SELECT interviewee_id
FROM INTERVIEWEE
WHERE city = 'Trenton' AND state = 'NJ';

SELECT report_num
FROM REPORT
WHERE type = 'trans_error';

SELECT report_num, report.usr_email, edit_metadata_description, decision                                            
FROM (report NATURAL JOIN METADATA_EDIT_REQUEST);

SELECT usr.usr_email, usr_username
FROM (USR NATURAL JOIN BLOCK);

/*INSERT COMMANDS FOUND in DATA.SQL*/

/*DELETE COMMANDS*/
DELETE FROM AUDIO_FILE /*successful after cascading*/
WHERE audio_file_id = 'JHS10SideA';

DELETE FROM INTERVIEWER/*successful after cascading*/
WHERE interviewer_id = 3;

DELETE FROM INTERVIEWEE/*successful after cascading*/
WHERE interviewee_id = 1;

DELETE FROM REPORT/*successful after cascading*/
WHERE report_num = 2;

DELETE FROM USR/*successful after cascading*/
WHERE usr_email = 'csanders@university.com';

DELETE FROM TRANSCRIPT
WHERE audio_file_id = 'JHS10SideA';

DELETE FROM KEYWORDS
WHERE audio_file_id = 'JHS10SideA';

DELETE FROM INTERVIEWER_RACES
WHERE interviewer_id = 3;

DELETE FROM INTERVIEWEE_RACES
WHERE interviewee_id = 1;

DELETE FROM TRANSCRIPT_ERROR
WHERE report_num = 2;

DELETE FROM METADATA_EDIT_REQUEST
WHERE report_num = 1;

UPDATE AUDIO_FILE
SET (title = 'new_title', description = 'new_descrip')
WHERE audio_file_id = 'JHS10SideA';

UPDATE INTERVIEWER
SET (name = 'new_name', gender = 'NG')
WHERE interviewer_id = 3;

UPDATE INTERVIEWEE
SET (name = 'new_name', gender = 'NG')
WHERE interviewee_id = 1;

UPDATE USR
SET (usr_username = 'new_username', user_password = 'new_password', is_blocked = 'Y')
WHERE user_email = 'csanders@university.com';

UPDATE ADMIN
SET (a_username = 'new_username', a_password = 'new_password')
WHERE a_email = 'mdonald@university.com';

UPDATE TRANSCRIPT
SET (transcriber = 'new_transcriber', t_language = 'new_language')
WHERE audio_file_id = 'JHS10SideA';

UPDATE KEYWORDS
SET (keyword = ARRAY['new_keyword'])
WHERE audio_file_id = 'JHS10SideA';

UPDATE INTERVIEWER_RACES
SET (race = 'new_race')
WHERE interviewer_id = 2;

UPDATE INTERVIEWEE_RACES
SET (race = 'new_race')
WHERE interviewee_id = 3;
