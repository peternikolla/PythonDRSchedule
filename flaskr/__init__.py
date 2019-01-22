import datetime

from flask import Flask, jsonify, request

# A series of lists of dicts that mimic SQL rows
doctors = [
    {'id': 0, 'first_name': 'John', 'last_name': 'Doe'},
    {'id': 1, 'first_name': 'Jane', 'last_name': 'Smith'}
]

locations = [
    {'id': 0, 'address': '123 Main St'},
    {'id': 1, 'address': '456 Central St'}
]

doctor_locations = [
    {'id': 0, 'doctor_id': 0, 'location_id': 0},
    {'id': 1, 'doctor_id': 1, 'location_id': 0},
    {'id': 2, 'doctor_id': 1, 'location_id': 1}
]

# Peter Start
# Hours doctors are available per DOW
# DOW 0 - Monday
doctor_hours = [
    {'id': 0, 'doctor_id': 0, 'DOW': 0, 'start': "08:00", "end": "17:00"},
    {'id': 1, 'doctor_id': 0, 'DOW': 1, 'start': "08:00", "end": "17:00"},
    {'id': 2, 'doctor_id': 1, 'DOW': 0, 'start': "09:00", "end": "15:00"}
]

# Id, Doctors Id, Location Id, Date, Time
doctor_schedules = [
    {'id': 0, 'doctor_id': 0, 'location_id': 0, 'date': '2019-01-21', 'time': '08:00'},
    {'id': 1, 'doctor_id': 0, 'location_id': 0, 'date': '2019-01-21', 'time': '08:30'}
]
# Peter End


# Program & structure influenced heavily by the Flask tutorial
# http://flask.pocoo.org/docs/1.0/tutorial/database/
def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    @app.route('/doctors', methods=['GET'])
    def list_doctors():
        """
        Get all doctors

        :return: List of full doctor entries
        """
        return jsonify(doctors), 200

    @app.route('/doctors/<int:doctor_id>', methods=['GET'])
    def list_doctor(doctor_id):
        """
        Get one doctor

        :param doctor_id: The id of the doctor
        :return: Full doctor entry
        """
        if doctor_id < 0 or doctor_id >= len(doctors):
            return jsonify({'message': 'Doctor not found'}), 404

        return jsonify(doctors[doctor_id]), 200

    # Note: Must set the content type to JSON. Use something like:
    # curl -X POST -H "Content-Type: application/json" --data '{"first_name": "Joe", "last_name": "Smith"}' http://localhost:5000/doctors
    @app.route('/doctors', methods=['POST'])
    def add_doctor():
        """
        Create a doctor

        :json-param first_name: The doctor's first name
        :json-param last_name: The doctor's last name

        :return: The id of the newly created doctor
        """
        req_data = request.get_json()

        try:
            first_name = req_data['first_name']
            last_name = req_data['last_name']
        except KeyError:
            return jsonify({'error_detail': 'Missing required field'}), 400

        # The id is simply the next index in the array
        doctor_id = len(doctors)

        doctors.append({'id': doctor_id, 'first_name': first_name, 'last_name': last_name})

        return jsonify({'id': doctor_id}), 200

    @app.route('/doctors/<int:doctor_id>/locations', methods=['GET'])
    def list_doctor_locations(doctor_id):
        """
        Get the locations for a single doctor

        :param doctor_id: The id of the doctor
        :return: List of full location entries
        """
        if doctor_id < 0 or doctor_id >= len(doctors):
            return jsonify({'message': 'Doctor not found'}), 404

        # Join locations via the doctor_locations "table" and doctor_id
        result = [locations[y['location_id']] for y in filter(lambda x: x['doctor_id'] != doctor_id, doctor_locations)]

        return jsonify(result), 200

    # Peter Start

    # Note: Must set the content type to JSON. Use something like:
    # curl -X POST -H "Content-Type: application/json" --data '{"doctor_id": 1, "location_id": 1, date": "2019-02-01", "time": "11:00"}' http://localhost:5000/appointment
    @app.route('/appointment', methods=['POST'])
    def add_appointment():
        """
        Add an appointment
        Appointment slots are 15 minutes

        :json-param doctor_id: The id of the doctor
        :json-param location_id: The location id of the Appointment
        :json-param date: YYYY-MM-DD Date of Appointment
        :json-param time: HH:MM Time of Appointment

        :return: success
        """
        req_data = request.get_json()

        try:
            doctor_id = req_data['doctor_id']
            location_id = req_data['location_id']
            date = req_data['date']
            time = req_data['time']
        except KeyError:
            return jsonify({'error_detail': 'Missing required field - doctor_id, location_id, date, time'}), 400

        # Validate doctor's Id
        if doctor_id < 0 or doctor_id >= len(doctors):
            return jsonify({'message': 'Doctor not found'}), 404

        # Valid Date and Time
        try:
            datetime_obj = datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M")
        except ValueError:
            return jsonify({'message': "Invalid date/time YYYY-MM-DD HH:MM"}), 404

        # Verify minutes are 00, 15 30 or 45 - Appointments are every 15 mines
        mins = datetime_obj.minute
        if mins not in {00, 15, 30, 45}:
            return jsonify({'message': "Minutes must be are 00, 15, 30 or 45"}), 404

        # TODO - Validate Location Id - This should ask be checked

        dow = datetime_obj.weekday()

        # Check if scheduled time is with in the doctor's hours for the DOW
        if len(list(filter(lambda x: x['start'] <= time <= x['end'] and x['DOW'] == dow and x['doctor_id'] == doctor_id, doctor_hours))) == 0:
            return jsonify({'message': "The DOW and/or time is not in the doctors schedule"}), 404

        # Check if the schedule time is already taken
        if len(list(filter(lambda x: date == x['date'] and time == x['time'] and x['doctor_id'] == doctor_id, doctor_schedules))) > 0:
            return jsonify({'message': "That appointment date and time is taken"}), 404

        # Add Appointment
        # The id is simply the next index in the array
        sched_id = len(doctor_schedules)
        doctor_schedules.append({'id': sched_id, 'doctor_id': doctor_id, 'location_id': location_id, 'date': date, "time": time})

        return jsonify("success"), 200

    @app.route('/appointments/<int:doctor_id>', methods=['GET'])
    def list_appointments(doctor_id):
        """
        Get the appointment for a single doctor

        :param doctor_id: The id of the doctor
        :return: success
        """
        if doctor_id < 0 or doctor_id >= len(doctors):
            return jsonify({'message': 'Doctor not found'}), 404

        # Get all Appointments for this doctor
        result = list(filter(lambda x: x['doctor_id'] == doctor_id, doctor_schedules))

        return jsonify(result), 200

    # Note: Must set the content type to JSON. Use something like:
    # curl -X DELETE -H "Content-Type: application/json" --data '{"doctor_id": 0, date": "2019-02-01", "time": "11:00"}' http://localhost:5000/appointment
    @app.route('/appointments', methods=['DELETE'])
    def cancel_appointment():
        """
        Cancel an appointment

        :json-param doctor_id: The id of the doctor
        :json-param date: YYYY-MM-DD Date of Appointment
        :json-param time: HH:MM Time of Appointment

        :return: success
        """

        req_data = request.get_json()

        try:
            doctor_id = req_data['doctor_id']
            date = req_data['date']
            time = req_data['time']
        except KeyError:
            return jsonify({'error_detail': 'Missing required field - doctor_id, date, time'}), 400

        index = 0
        for sch in doctor_schedules:
            if sch['doctor_id'] == doctor_id and sch['date'] == date and sch['time'] == time:
                doctor_schedules.pop(index)
                return jsonify('success'), 200
            index += 1

            return jsonify({'message': 'Nothing scheduled for that time'}), 404

    # Peter End

    return app
