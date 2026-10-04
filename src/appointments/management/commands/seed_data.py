import random
from datetime import date, datetime, time, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from appointments.models import Doctor, Patient, TimeSlot


class Command(BaseCommand):
    help = "Generate synthetic doctors, patients and time slots."

    def add_arguments(self, parser):
        parser.add_argument(
            "--doctors",
            type=int,
            default=10,
            help="Number of doctors to create.",
        )

        parser.add_argument(
            "--patients",
            type=int,
            default=100,
            help="Number of patients to create.",
        )

        parser.add_argument(
            "--days",
            type=int,
            default=14,
            help="Number of days of time slots to generate.",
        )

    @transaction.atomic
    def handle(self, *args, **options):

        number_of_doctors = options["doctors"]
        number_of_patients = options["patients"]
        number_of_days = options["days"]

        self.stdout.write(
            self.style.WARNING("Generating synthetic data...")
        )

        # ---------------------------------------------------------
        # DATA
        # ---------------------------------------------------------

        first_names_male = [
            "Adam", "Yassine", "Omar", "Amine", "Mehdi",
            "Ayoub", "Hamza", "Anas", "Zakaria", "Ilyas",
        ]

        first_names_female = [
            "Sara", "Salma", "Aya", "Nour", "Imane",
            "Hiba", "Maryam", "Lina", "Chaimae", "Nada",
        ]

        last_names = [
            "Alaoui", "Bennani", "El Amrani", "Tazi",
            "Idrissi", "Berrada", "Chraibi", "Fassi",
            "Naciri", "Tahiri",
        ]

        specializations = [
            "Cardiology",
            "Dermatology",
            "General Medicine",
            "Neurology",
            "Pediatrics",
            "Psychiatry",
            "Orthopedics",
            "Ophthalmology",
            "Gastroenterology",
            "Endocrinology",
        ]

        cities = [
            "Casablanca",
            "Rabat",
            "Marrakesh",
            "Fes",
            "Tangier",
            "Agadir",
            "Meknes",
            "Oujda",
        ]

        neighborhoods = {
            "Casablanca": [
                "Maarif",
                "Anfa",
                "Bourgogne",
                "Gauthier",
                "Sidi Maarouf",
            ],
            "Rabat": [
                "Agdal",
                "Hassan",
                "Hay Riad",
                "Souissi",
            ],
            "Marrakesh": [
                "Gueliz",
                "Medina",
                "Daoudiate",
            ],
            "Fes": [
                "Ville Nouvelle",
                "Agdal",
                "Narjiss",
            ],
            "Tangier": [
                "Iberia",
                "Malabata",
                "Mesnana",
            ],
            "Agadir": [
                "Talborjt",
                "Hay Mohammadi",
                "Dakhla",
            ],
            "Meknes": [
                "Hamria",
                "Marjane",
                "Belle Vue",
            ],
            "Oujda": [
                "Centre Ville",
                "Al Qods",
                "Hay Al Irfane",
            ],
        }

        # ---------------------------------------------------------
        # DOCTORS
        # ---------------------------------------------------------

        doctors = []

        for i in range(number_of_doctors):

            first_name = random.choice(first_names_male + first_names_female)
            last_name = random.choice(last_names)

            username = f"doctor_{i + 1}"

            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=f"{username}@example.com",
                password="TestPassword123!",
            )

            doctor = Doctor.objects.create(
                user=user,
                specialization=random.choice(specializations),
                appointment_duration=random.choice([20, 30, 30, 30, 45]),
            )

            doctors.append(doctor)

        # ---------------------------------------------------------
        # PATIENTS
        # ---------------------------------------------------------

        for i in range(number_of_patients):

            gender = random.choice(["M", "F"])

            if gender == "M":
                first_name = random.choice(first_names_male)
            else:
                first_name = random.choice(first_names_female)

            last_name = random.choice(last_names)

            username = f"patient_{i + 1}"

            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=f"{username}@example.com",
                password="TestPassword123!",
            )

            # Patient age between 18 and 80
            age = random.randint(18, 80)

            today = date.today()

            birth_year = today.year - age

            birth_date = date(
                birth_year,
                random.randint(1, 12),
                random.randint(1, 28),
            )

            city = random.choice(cities)

            Patient.objects.create(
                user=user,
                birth_date=birth_date,
                gender=gender,
                phone=f"06{random.randint(10000000, 99999999)}",
                city=city,
                neighborhood=random.choice(neighborhoods[city]),
                diabetes=random.random() < 0.10,
                hypertension=random.random() < 0.15,
                handicapped=random.random() < 0.05,
                email_verified=True,
            )

        # ---------------------------------------------------------
        # TIME SLOTS
        # ---------------------------------------------------------

        today = date.today()

        total_slots = 0

        for doctor in doctors:

            duration = doctor.appointment_duration

            for day_offset in range(number_of_days):

                current_date = today + timedelta(days=day_offset)

                # Skip weekends
                if current_date.weekday() >= 5:
                    continue

                current_time = datetime.combine(
                    current_date,
                    time(9, 0)
                )

                end_of_morning = datetime.combine(
                    current_date,
                    time(12, 30)
                )

                start_of_afternoon = datetime.combine(
                    current_date,
                    time(14, 0)
                )

                end_of_day = datetime.combine(
                    current_date,
                    time(17, 0)
                )

                # Morning slots
                while current_time + timedelta(minutes=duration) <= end_of_morning:

                    slot_end = current_time + timedelta(minutes=duration)

                    TimeSlot.objects.create(
                        doctor=doctor,
                        date=current_date,
                        start_time=current_time.time(),
                        end_time=slot_end.time(),
                        is_available=True,
                    )

                    total_slots += 1
                    current_time = slot_end

                # Afternoon
                current_time = start_of_afternoon

                while current_time + timedelta(minutes=duration) <= end_of_day:

                    slot_end = current_time + timedelta(minutes=duration)

                    TimeSlot.objects.create(
                        doctor=doctor,
                        date=current_date,
                        start_time=current_time.time(),
                        end_time=slot_end.time(),
                        is_available=True,
                    )

                    total_slots += 1
                    current_time = slot_end

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {len(doctors)} doctors, "
                f"{number_of_patients} patients and "
                f"{total_slots} time slots."
            )
        )