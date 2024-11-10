from collections import namedtuple
from contextlib import nullcontext
from os import walk

from repositories import user
from repositories.patient import Patient;
from typing import List

from flask import Flask, request, jsonify
from repositories.session_manager import SessionManager
from repositories.workers import Worker
from repositories.user import UserInfo
from datetime import datetime

class System:
    # def __init__(self):
        # self.permission_manager = PermissionManager()
        # self.session_manager = SessionManager()
        # self.monitors_list: List[Monitor] = []
        # self.report_list: List[Report] = []
        # self.exams_list: List[Exam] = []
        # self.results_list: List[Result] = []

    def create_patient_account(self,patientName: str, email: str, phoneNumber: str, dob: str, docID: int, password: str):

        date_object = datetime.strptime(dob, "%Y-%m-%d").date()
        newPatient = Patient(patientName, email, phoneNumber, date_object, docID, password)
        status = newPatient.create_patient()

        return jsonify({
                'confirm': status.name
            })


    def log_in(self, userType: str, email: str, password: str):
        if userType == "patient":  # Patient
            user_info = Patient.get_user_record(email, password)
        elif userType == "worker":  # Worker
            user_info = Worker.get_user_record(email, password)
        else:
            return jsonify({
                'error': 'Invalid user type'
            }), 400  # Return an error response for invalid user type

        if user_info is None:  # If the patient is not approved
            return jsonify({
                'error': 'Your account is not approved yet. Please contact support.'
            }), 403  # 403 Forbidden: The patient is not approved.

        if user_info.user_type.value != "Error":
            return jsonify({
                'login': {
                    'routeTo': user_info.user_type.value,
                    'email': user_info.email,
                    'id': user_info.id,
                }
            })
        return None
            # NOT IN USE
            #token = SessionManager.generate_token(user_info.email)
            #SessionManager.create_session(token, user_info.email, user_info.user_type.value)
            # NOT IN USE

    # NOT IN USE

    #def token_required(self, token: str):
    #    user_info: UserInfo
    #    user_info = SessionManager.decode_token(token)
    #    if (user_info.user_type.value == "Administrator" and
    #      user_info.user_type.value == "Staff" and
    #      user_info.user_type.value == "Doctor"):
    #        Worker.get_user_record(user_info.email, user_info.password)
    #        # return conformation
    #    elif (user_info.user_type.value == "Patient"):
    #        Patient.get_user_record(user_info.email, user_info.password)
    #        # return conformation
    #    else:
    #        return "error"

    # NOT IN USE

    def get_doc_list_form(self):
        result = Worker.get_doctors_list()

        doctor_list = [{
            'id': info.id,
            'email': info.email,
        } for info in result]

        return jsonify(doctor_list)


    def view_patient(self, id: int):
        try:
            # Get the patient record from the Patient class
            patient = Patient.get_user_record_profile(id)
    
            if patient:
                # Return the formatted response in JSON format
                return jsonify({
                    'id': patient.id,
                    'name': patient.name,
                    'email': patient.email,
                    'dob': patient.dob,
                    'status': patient.status,
                    'doctor_id': patient.id,
                    'phone': patient.phone,
                })
            else:
                return jsonify({'error': 'Patient not found'}), 404
    
        except Exception as e:
            return jsonify({'error': f'Something went wrong: {str(e)}'}), 500


    def update_patient_profile(self, id: int, data: dict):
        try:
            # Assuming `Patient` has a method to update profile
            updated_patient = Patient.update_user_record_profile(id, data)
    
            if updated_patient:
                return updated_patient
            else:
                return None
        except Exception as e:
            raise Exception(f"Error updating patient profile: {str(e)}")

    def view_all_patients(self):
        try:
            # Fetch list of pending patients from Patient class
            patients = Patient.give_list_of_pending()
            
            if patients:
                # Format the patient data for frontend
                patient_list = [{
                    'healthid': patient[0],  # Patient ID from the DB
                    'patientname': patient[1],
                    'email': patient[2],
                    'status': patient[3]
                } for patient in patients]
                
                return jsonify(patient_list)
            else:
                return jsonify({'message': 'No pending patients found'}), 404
        except Exception as e:
            return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
    
    def update_patient_account_status(self, patient_id: int):
        try:
            # Approve the patient by updating the status to True
            Patient.approve_patient(patient_id)
            return jsonify({'message': 'Patient approved successfully'}), 200
        except Exception as e:
            return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

    def view_worker(self, id: int):
        try:
            # Get worker record from Worker class
            worker = Worker.get_user_record_profile(id)
    
            if worker:
                # Return the worker data as JSON
                return jsonify({
                    'id': worker.id,
                    'name': worker.name,
                    'email': worker.email,
                    'phone': worker.phone,
                    'image': worker.image,  # You may choose to encode the image
                    'user_type': worker.user_type
                })
            else:
                return jsonify({'error': 'Worker not found'}), 404
        except Exception as e:
            return jsonify({'error': f'Something went wrong: {str(e)}'}), 500
    
    def update_worker_account(self, id: int, data: dict):
        try:
            # Update the worker's information through the Worker class
            updated_worker = Worker.update_user_record_profile(id, data)
    
            if updated_worker:
                return jsonify({
                    'message': 'Worker profile updated successfully',
                    'worker': {
                        'id': updated_worker.id,
                        'name': updated_worker.name,
                        'email': updated_worker.email,
                        'phone': updated_worker.phone,
                        'user_type': updated_worker.user_type
                    }
                }), 200
            else:
                return jsonify({'error': 'Worker not found'}), 404
        except Exception as e:
            return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

    def view_all_workers(self):

        # ...
        return jsonify({
            'temp': 'temp'
        })

    def create_worker_account(self, id: int):
        return jsonify({
            'temp': 'temp'
        })
            
    def delete_worker_account(self):
        return jsonify({
            'temp': 'temp'
        })

    def delete_patient_account(self):
        return jsonify({
            'temp': 'temp'
        })

    def view_exam(self):
        return jsonify({
            'temp': 'temp'
        })

    def doctors_patients(self):
        return jsonify({
            'temp': 'temp'
        })

    def prescribe_exam(self):
        return jsonify({
            'temp': 'temp'
        })
    
    def view_results(self, id: int, userType: str):
        return jsonify({
            'temp': 'temp'
        })

    def view_all_results(self):
        return jsonify({
            'temp': 'temp'
        })

    def create_results(self):
    #def create_results(self, staff: Worker, patient: Patient):
        return jsonify({
            'temp': 'temp'
        })
    
    def delete_results(self):
    # def delete_results(self, result_id: int):
        return jsonify({
            'temp': 'temp'
        })
    
    def view_year_n_month_reports(self):
        return jsonify({
            'temp': 'temp'
        })
    
    def create_year_n_month_reports(self):
    #def create_reports(self, admin: Worker):
        return jsonify({
            'temp': 'temp'
        })

    def view_predict_reports(self):
        return jsonify({
            'temp': 'temp'
        })
    
    def create_predict_reports(self):
    #def create_reports(self, admin: Worker):
        return jsonify({
            'temp': 'temp'
        })

#
#    def delete_report(self):
#    #def delete_report(self, report_id: int):
#        return jsonify({
#            'temp': 'temp'
#        })

    def view_smart_monitor(self):
        return jsonify({
            'temp': 'temp'
        })

    def create_smart_monitor(self):
    #def create_smart_monitor(self, doctor: Worker, options: List[str]):
        return jsonify({
            'temp': 'temp'
        })
 
    
    def change_smart_monitor(self):
    #def change_smart_monitor(self, doctor: Worker, options: List[str]):
        return jsonify({
            'temp': 'temp'
        })
 
    def delete_smart_monitor(self):
    #def delete_smart_monitor(self, monitor_id: int):
         return jsonify({
            'temp': 'temp'
        })
    

