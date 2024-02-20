from models import *

class Db_Build():
    # This script populates the database, run from Flask shell
    @staticmethod
    def db_init_all():
        Db_Build.db_init_user()
        Db_Build.db_init_breed_info()
        Db_Build.db_init_breed_notes()

    @staticmethod
    def db_init_user():
        user_list = []
        user_list.append(User("id"))
        for user in user_list:
            db.session.add(user)
        db.session.commit()
    
    @staticmethod
    def db_init_breed_info():
        breed_info_list = []
        breed_info_list.append(BreedInfo("breed_id"))
        breed_info_list.append(BreedInfo("breed_name"))
        breed_info_list.append(BreedInfo("breed_group"))
        breed_info_list.append(BreedInfo("life_span"))
        breed_info_list.append(BreedInfo("weight"))
        breed_info_list.append(BreedInfo("height"))
        breed_info_list.append(BreedInfo("bred_for"))
        breed_info_list.append(BreedInfo("temperament"))
        breed_info_list.append(BreedInfo("reference_image_id"))
        breed_info_list.append(BreedInfo("user_token"))
        for breed_info in breed_info_list:
            db.session.add(breed_info)
        db.session.commit()
    
    @staticmethod
    def db_init_breed_notes():
        breed_notes_list = []
        breed_notes_list.append(BreedNotes("notes"))
        breed_notes_list.append(BreedNotes("id"))
        breed_notes_list.append(BreedNotes("breed_id"))
        breed_notes_list.append(BreedNotes("user_token"))
        breed_notes_list.append(BreedNotes("breedNotes_Id"))
        for breed_notes in breed_notes_list:
            db.session.add(breed_notes)
        db.session.commit()

class Db_Destroy():
    # This script destoys the database, run from Flask shell
    @staticmethod
    def db_destroy():
        db.reflect()
        db.drop_all()