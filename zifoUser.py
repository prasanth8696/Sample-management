import os
import datetime
from zifoDatabase import session,Sample

class ZifoUser :


  def clear(self) :
    clear_val = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear_val)

  # Register samples...
  def addSamples(self,author) :
     if author.role == 'LAB' :
       print('you dont have rights to do add samples... ')
       return
     try :
       name = input('Enter Reagents name ')
       quantity = input('Enter quantity in kg(Liguid also)  ')
       type = int(input('enter type of reactive 1 => reactive,0 => Non reactive '))
       expire_days = int(input('Enter no of days to expire '))
       if type > 1 and type < 0 :
         raise ValueError
     except ValueError :
        self.clear()
        print('Invalid Input...')
        self.addSamples(author)
        return
     except Exception :
        print('Something went Wrong...')
        return
     type = bool(type)
     new_samples = Sample(
             name = name,
             quantity = quantity,
             reactive = type,
             entry_date = datetime.datetime.now(),
             expire_date = datetime.datetime.now() + datetime.timedelta(days=expire_days),
             author = author
            )
     session.add(new_samples)
     session.commit()
     print('Sample added sucessfully...')
     return

  #get only my samples
  def getMySamples(self,author):
    self.clear()
    if author.role == 'LAB' :
       print('you dont have rights to do add samples...')
       return
    samples = session.query(Sample).filter(Sample.author_id == author.id).all()
    if samples == [] :
      print('You dont have any samples...')
      return

    print('Id     name       Type      quantity(kg)      addedDate      Expirein        author') 
    reactive = 0;non_reactive = 0
    for sample in samples :
       if sample.reactive == True :
         reactive += 1
       else:
         non_reactive += 1
       print(str(sample.id).ljust(5),end='')
       print(sample.name.ljust(10),end='')
       type =  'Reactive' if sample.reactive else 'Non-reactive'
       print(type.ljust(14),end='')
       print(sample.quantity.ljust(10),end='')
       addedDate = str(sample.entry_date.date())
       print(addedDate.ljust(14),end='')
       if datetime.datetime.now() > sample.expire_date :
         expireIn = 'Expired'
       else:
         expireTime =sample.expire_date - datetime.datetime.now()
         expireIn = str(expireTime.days) + 'days ' + str(expireTime.seconds) + 'sec'

       print(str(expireIn).ljust(18),end='')
       print(author.id.ljust(14),end='')
       print('\n')
    print()
    print(f'your Total samples {len(samples)}')
    print(f'reactive samples {reactive}')
    print(f'None Reactive samples {non_reactive}')

   # Get all samples in the database...
  def getAllSamples(self,author):
    self.clear()
    samples = session.query(Sample).all()
    if samples == [] :
      print('Currently No Samples available...')
      return

    print('Id      name       Type     quantity(Kg)      addedDate      Expirein       author')
    reactive = 0;non_reactive = 0
    for sample in samples :
       if sample.reactive == True :
         reactive += 1
       else:
         non_reactive += 1
       print(str(sample.id).ljust(5),end='')
       print(sample.name.ljust(10),end='')
       type =  'Reactive' if sample.reactive else 'Non-reactive'
       print(type.ljust(14),end='')
       print(sample.quantity.ljust(10),end='')
       addedDate = str(sample.entry_date.date())
       print(addedDate.ljust(14),end='')
       if datetime.datetime.now() > sample.expire_date :
            expireIn = 'Expired'
       else :
            expireTime = sample.expire_date - datetime.datetime.now()
            expireIn = f'{expireTime.days}days {expireTime.seconds} sec'
       print(str(expireIn).ljust(18),end='')
       print(author.id.ljust(14),end='')
       print('\n')
    print()
    print(f'Total samples {len(samples)}')
    print(f'reactive samples {reactive}')
    print(f'None Reactive samples {non_reactive}')

  #Update samples...
  def updateSamples(self,author) :
    if author.role == 'LAB' :
      print('you dont have permissions to update the samples...')
      return
    #Input Exception
    try :
       sample_id = int(input('Enter sample id '))
    except ValueError :
       self.clear()
       print('Invalid Input...')
       self.updateSamples(author)
       return

    sample = session.query(Sample).filter(sample_id == sample_id).first()
    if sample is None :
      print('Inavlid sample Id...')
      return
    if sample.author_id != author.id :
      print('you dont have permissions to update another person samples')
      return
    expire = int(input('add new samples ,enter new expirey days'))
    quantity = input('Enter quantity in kg ')
    new_expire = datetime.datetime.now() + datetime.timedelta(expire)
    sample.entry_date = datetime.datetime.now()
    sample.expire_date = new_expire
    sample.quantity = quantity
    session.commit()
    print('Sample succesfully updated...')

  # Delete sampels
  def deleteSamples(self,author):
    if author.role == 'LAB' :
      print('you dont have permissions to delete the samples...')
      return
    try :
      sample_id = int(input('Enter Sample Id '))
    except ValueError :
      self.clear()
      print('Invalid Input...')
      self.deleteSamples(author)
      return
    sample = session.query(Sample).filter(Sample.id == sample_id).first()
    if sample is None :
      print('Inavalid sample Id...')
      return
    if sample.author_id != author.id :
      print('you dont have permissions to delete another person samples ...')
      return
    session.delete(sample)
    session.commit()
    print('Sample deleted Successfully...')

  # print which samples will expired in 15 days...
  def printExpireSamples(self,user) :
    if user.role == 'LAB' :
       samples = session.query(Sample).all()
    else :
       samples = session.query(Sample).filter(Sample.author_id == user.id).all()
    if samples is None :
      return
    print('Expire Notifications\n' )
    print('Id        name             ExpireIn  ')
    for sample in samples :
          expire_days = sample.expire_date - datetime.datetime.now()
          if expire_days.days <= 15 :
             print(str(sample.id).ljust(10),end='')
             print(sample.name.ljust(15),end='')
             print(expire_days,end='')
             print('\n')

    print('\n')
