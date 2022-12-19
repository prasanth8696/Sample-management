import os
import csv
import datetime
from zifoDatabase import session, Sample, Users
from style import *
from colorama import init

init(autoreset=True)


class ZifoUser:
    def clear(self):
        clear_val = "cls" if os.name == "nt" else "clear"
        os.system(clear_val)

    # Register samples...
    def addSamples(self, author):
        if author.role == "LAB":
            print(red + "you dont have rights to do add samples... ")
            return
        try:
            name = input(yellow + "Enter Reagents name " + normal).strip()
            quantity = input(
                yellow + "Enter quantity in kg(Liguid also)  " + normal
            ).strip()
            type = int(
                input(
                    yellow
                    + "enter type of reactive 1 => reactive,0 => Non reactive "
                    + normal
                ).strip()
            )
            expire_days = int(
                input(yellow + "Enter no of days to expire " + normal).strip()
            )
            if type > 1 and type < 0:
                raise ValueError
        except ValueError:
            self.clear()
            print(red + "Invalid Input...")
            self.addSamples(author)
            return
        except KeyboardInterrupt:
            self.clear()
            print("program sucessfully exited using KeyboardInterrupt")
            exit()
        except Exception:
            print(red + "Something went Wrong...")
            return
        type = bool(type)
        new_samples = Sample(
            name=name,
            quantity=quantity,
            reactive=type,
            entry_date=datetime.datetime.now(),
            expire_date=datetime.datetime.now() + datetime.timedelta(days=expire_days),
            author=author,
        )
        session.add(new_samples)
        session.commit()
        self.clear()
        print(green + "Sample added sucessfully...")
        return

    # get only my samples
    def getMySamples(self, author):
        self.clear()
        if author.role == "LAB":
            print(red + "you dont have rights to do add samples...")
            return
        samples = session.query(Sample).filter(Sample.author_id == author.id).all()
        if samples == []:
            print(green + "You dont have any samples...")
            return

        print(
            sky_blue
            + "Id     name       Type      quantity(kg)      addedDate      Expirein        author"
        )
        reactive = 0
        non_reactive = 0
        for sample in samples:
            if sample.reactive == True:
                reactive += 1
            else:
                non_reactive += 1
            print(str(sample.id).ljust(5), end="")
            print(sample.name.ljust(10), end="")
            type = "Reactive" if sample.reactive else "Non-reactive"
            print(type.ljust(14), end="")
            print(sample.quantity.ljust(10), end="")
            addedDate = str(sample.entry_date.date())
            print(addedDate.ljust(14), end="")
            if datetime.datetime.now() > sample.expire_date:
                expireIn = red + "Expired"
            else:
                expireTime = sample.expire_date - datetime.datetime.now()
                if expireTime.days < 15:
                    expireIn = (
                        red
                        + str(expireTime.days)
                        + "days "
                        + str(expireTime.seconds)
                        + "sec"
                    )
                else:
                    expireIn = (
                        green
                        + str(expireTime.days)
                        + "days "
                        + str(expireTime.seconds)
                        + "sec"
                    )

            print(str(expireIn).ljust(30), end="")
            print(author.id.rjust(7), end="")
            print("\n")
        print()
        print(f"your Total samples {len(samples)}")
        print(f"reactive samples {reactive}")
        print(f"None Reactive samples {non_reactive}")

    # Get all samples in the database...
    def getAllSamples(self, author):
        self.clear()
        samples = session.query(Sample).all()
        if samples == []:
            print(green + "Currently No Samples available...")
            return

        print(
            sky_blue
            + "Id      name       Type     quantity(Kg)      addedDate      Expirein       author"
        )
        reactive = 0
        non_reactive = 0
        for sample in samples:
            if sample.reactive == True:
                reactive += 1
            else:
                non_reactive += 1
            print(str(sample.id).ljust(5), end="")
            print(sample.name.ljust(10), end="")
            type = "Reactive" if sample.reactive else "Non-reactive"
            print(type.ljust(14), end="")
            print(sample.quantity.ljust(10), end="")
            addedDate = str(sample.entry_date.date())
            print(addedDate.ljust(14), end="")
            if datetime.datetime.now() > sample.expire_date:
                expireIn = red + "Expired"
            else:
                expireTime = sample.expire_date - datetime.datetime.now()
                if expireTime.days < 15:
                    expireIn = red + f"{expireTime.days}days {expireTime.seconds} sec"
                else:
                    expireIn = green + f"{expireTime.days}days {expireTime.seconds} sec"
            print(str(expireIn).ljust(30), end="")
            print(author.id.rjust(7), end="")
            print("\n")
        print()
        print(f"Total samples {len(samples)}")
        print(f"reactive samples {reactive}")
        print(f"None Reactive samples {non_reactive}")

    # Update samples...
    def updateSamples(self, author):
        if author.role == "LAB":
            print(red + "you dont have permissions to update the samples...")
            return
        # Input Exception
        try:
            sample_id = int(input(yellow + "Enter sample id " + normal).strip())
        except ValueError:
            self.clear()
            print(red + "Invalid Input...")
            self.updateSamples(author)
            return

        sample = session.query(Sample).filter(sample_id == sample_id).first()
        if sample is None:
            print(red + "Invalid sample Id...")
            return
        if sample.author_id != author.id:
            print(red + "you dont have permissions to update another person samples")
            return
        expire = int(input(yellow + "add new samples ,enter new expirey days" + normal))
        quantity = input(yellow + "Enter quantity in kg " + normal)
        new_expire = datetime.datetime.now() + datetime.timedelta(expire)
        sample.entry_date = datetime.datetime.now()
        sample.expire_date = new_expire
        sample.quantity = quantity
        session.commit()
        print(green + "Sample succesfully updated...")

    # Delete sampels
    def deleteSamples(self, author):
        if author.role == "LAB":
            print(red + "you dont have permissions to delete the samples...")
            return
        try:
            sample_id = int(input(yellow + "Enter Sample Id " + normal).strip())
        except ValueError:
            self.clear()
            print(red + "Invalid Input...")
            self.deleteSamples(author)
            return
        sample = session.query(Sample).filter(Sample.id == sample_id).first()
        if sample is None:
            print(red + "Invalid sample Id...")
            return
        elif not sample.author:
            session.delete(sample)
            session.commit()
            print(green + "Unknown sample deleted sucessfully...")
            return
        elif sample.author_id != author.id:
            print(
                red + "you dont have permissions to delete another person samples ..."
            )
            return
        session.delete(sample)
        session.commit()
        print(green + "Sample deleted Successfully...")

    # print which samples will expired in 15 days...
    def printExpireSamples(self, user):
        if user.role == "LAB":
            samples = session.query(Sample).all()
        else:
            samples = session.query(Sample).filter(Sample.author_id == user.id).all()
        if samples is None:
            return
        print(red + "Expire Notifications\n")
        print(sky_blue + "Id        name             ExpireIn  ")
        for sample in samples:
            expire_days = sample.expire_date - datetime.datetime.now()
            if expire_days.days <= 15:
                print(str(sample.id).ljust(10), end="")
                print(sample.name.ljust(15), end="")
                print(red + str(expire_days), end="")
                print("\n")

        print("\n")

    # createReport for Samples(Scientist and Lab tech will use this method)
    def generateReport(self, id):
        user = session.query(Users).filter(Users.id == id).first()
        if user is None:
            print(red + "Invalid User...")
        samples = session.query(Sample).all()
        # check samples are available or not if not available raise exception
        if not samples:
            print(red + "Currently No samples Available report cannot be generated... ")
            return
        # File name creation
        if user.role == "SCI":
            fileName = (
                f"{user.id}({user.employee.name})-{datetime.datetime.now()}_report.csv"
            )
        else:
            fileName = (
                f"{user.id}({user.employee.name})-{datetime.datetime.now()}_report.csv"
            )

        fieldnames = [
            "ID",
            "NAME",
            "TYPE",
            "QUANTITY(KG)",
            "ADDED_DATE",
            "EXPIRE_DATE",
            "EXPIRE_IN",
            "AUTHOR_ID",
            "EMPLOYEE_ID",
        ]
        if not os.path.exists("reports"):
            os.makedirs("reports")
        cwd = os.getcwd()
        path = os.path.join(cwd, f"reports/{fileName}")
        with open(path, "w") as reportFile:
            csv_writer = csv.DictWriter(reportFile, fieldnames=fieldnames)
            # initilize the header
            csv_writer.writeheader()

            for sample in samples:
                sampleDetail = sample.reportList()
                csv_writer.writerow(sampleDetail)
        print(f"{pink} {fileName} {green} created sucessfully...")
