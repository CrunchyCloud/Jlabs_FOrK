from repositories.db_service import DBService

class Exam:
    @staticmethod
    def fetch_test_types(exam_id):
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT testtype FROM presecribedTest WHERE examId = %s
        """, (exam_id,))
        test_types = cursor.fetchall()

        cursor.close()
        conn.close()

        return [test_type[0] for test_type in test_types]

    @staticmethod
    def fetch_exams_with_patient_info():
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT e.examid, e.examtype, p.patientname, p.email 
            FROM examtable e
            JOIN patient p ON e.healthid = p.healthid
        """)  # Fetch exam details along with patient info
        exams = cursor.fetchall()

        exams_list = [{
            'examid': exam[0],
            'examtype': exam[1],
            'patient_name': exam[2],
            'patient_email': exam[3]
        } for exam in exams]

        cursor.close()
        conn.close()

        return exams_list

    @staticmethod
    def fetch_exams():
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM examtable")  # Fetch all exams
        exams = cursor.fetchall()

        # Format the results in a more usable form
        exams_list = [{
            'examid': exam[0],
            'examtype': exam[4],  # Assuming the exam type is in the 5th column (index 4)
            'notes': exam[5]  # Assuming there are notes available
        } for exam in exams]

        cursor.close()
        conn.close()

        return exams_list

    @staticmethod
    def fetch_exam_types():
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT examtype FROM examtype")  # Fetch all exam types
        exam_types = cursor.fetchall()

        # Return exam types as a list
        exam_types_list = [exam[0] for exam in exam_types]

        cursor.close()
        conn.close()
        return exam_types_list


    #@staticmethod
    #def fetch_test_types():
    #    db = DBService()
    #    conn = db.get_db_connection()
    #    cursor = conn.cursor()
    #
    #    # Fetch all test types related to blood tests, filtering based on the 'Blood Test' exam type
    #    cursor.execute("SELECT * FROM testtypes;")
    #    test_types = cursor.fetchall()
    #
    #    # Return test types as a list
    #    test_types_list = [test[0] for test in test_types]
    #
    #    cursor.close()
    #    conn.close()
    #    return test_types_list



    @staticmethod
    def prescribe_exam(data):
        exam_type = data.get('examType')
        healthid = data.get('patientId')  # Patient ID
        workersid = data.get('doctorId')  # Doctor's ID (logged in user)
        content = data.get('content')  # Exam content (e.g., notes)
        test_types = data.get('testTypes', [])  # List of test types
        
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
    
        # If exam type is "Blood", check if there's an existing exam for this patient
        if exam_type == 'Blood':
            cursor.execute(
                "SELECT examid FROM examtable WHERE healthid = %s AND examtype = %s ORDER BY examdate DESC LIMIT 1",
                (healthid, exam_type)
            )
            existing_exam = cursor.fetchone()
    
            # If an existing exam is found, use that examId, else create a new exam
            if existing_exam:
                exam_id = existing_exam[0]
            else:
                cursor.execute(
                    "INSERT INTO examtable (examdate, healthid, workersid, examtype, notes) VALUES (CURRENT_DATE, %s, %s, %s, %s) RETURNING examid",
                    (healthid, workersid, exam_type, content)
                )
                exam_id = cursor.fetchone()[0]
        else:
            # For other exam types, create a new exam entry as usual
            cursor.execute(
                "INSERT INTO examtable (examdate, healthid, workersid, examtype, notes) VALUES (CURRENT_DATE, %s, %s, %s, %s) RETURNING examid",
                (healthid, workersid, exam_type, content)
            )
            exam_id = cursor.fetchone()[0]
    
        # Insert prescribed test types for this exam
        for test_type in test_types:
            cursor.execute(
                "INSERT INTO presecribedTest (examid, testtype) VALUES (%s, %s)",
                (exam_id, test_type)
            )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return exam_id
    @staticmethod
    def return_test_types_with_examtype():
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()
    
        cursor.execute("SELECT testtype, examtype FROM testtypes")
        test_types = cursor.fetchall()
    
        test_type_list = [{
            'testtype': test[0],
            'examtype': test[1]
        } for test in test_types]
    
        cursor.close()
        conn.close()
    
        return test_type_list

    @staticmethod
    def fetch_test_types(exam_id):
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT presecribedTest.testtype FROM presecribedTest
            LEFT JOIN testresults ON ((presecribedTest.examid = testresults.examid) AND(presecribedTest.testtype = testresults.testtype))
            WHERE presecribedTest.examId = %s AND testresults.results IS NULL
        """, (exam_id,))
        test_types = cursor.fetchall()

        cursor.close()
        conn.close()

        return [test_type[0] for test_type in test_types]

    @staticmethod
    def fetch_test_types_update(exam_id):
        db = DBService()
        conn = db.get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT presecribedTest.testtype FROM presecribedTest
            LEFT JOIN testresults ON ((presecribedTest.examid = testresults.examid) AND(presecribedTest.testtype = testresults.testtype))
            WHERE presecribedTest.examId = %s AND testresults.results IS NOT NULL
        """, (exam_id,))
        test_types = cursor.fetchall()

        cursor.close()
        conn.close()

        return [test_type[0] for test_type in test_types]
