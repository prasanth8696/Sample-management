import os
import datetime
from zifoDatabase import session,Sample

class ZifoUser :


  def clear(self) :
    clear_val = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear_val)


  def addSamples(self,author) :
     if author.role == 'LAB' :
       print('you dont have rights to do add samples... ')
       return
     try :
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
             reactive = type,
             entry_date = datetime.datetime.now(),
             expire_date = datetime.datetime.now() + datetime.timedelta(days=expire_days),
             author = author
            )
     session.add(new_samples)
     session.commit()
     print('Sample added sucessfully...')
     return


  def getMySamples(self,author):
    self.clear()
    if author.role == 'LAB' :
       print('you dont have rights to do add samples...')
       return
    samples = session.query(Sample).filter(Sample.author_id == author.id).all()
    if samples == [] :
      print('You dont have any samples...')
      return

    print('Id     Type        addedDate      Expirein        author') 
    reactive = 0;non_reactive = 0
    for sample in samples :
       if sample.reactive == True :
         reactive += 1
       else:
         non_reactive += 1
       print(str(sample.id).ljust(5),end='')
       type =  'Reactive' if sample.reactive else 'Non-reactive'
       print(type.ljust(14),end='')
       addedDate = str(sample.entry_date.date())
       print(addedDate.ljust(14),end='')
       if datetime.datetime.now() > sample.expire_date :
         expireIn = 'Expired'
       else:
         expireTime = datetime.datetime.now() - sample.expire_date
         expireIn = str(expireTime.days) + ' days ' + str(expireTime.seconds) + ' Seconds'

       print(str(expireIn).ljust(18),end='')
       print(author.id.ljust(14),end='')
       print()
    print()
    print(f'your Total samples {len(samples)}')
    print(f'reactive samples {reactive}')
    print(f'None Reactive samples {non_reactive}')


  def getAllSamples(self,author):
    self.clear()
    samples = session.query(Sample).all()
    if samples == [] :
      print('Currently No Samples available...')
      return

    print('Id      Type        addedDate      Expirein       author')
    reactive = 0;non_reactive = 0
    for sample in samples :
       if sample.reactive == True :
         reactive += 1
       else:
         non_reactive += 1
       print(str(sample.id).ljust(5),end='')
       type =  'Reactive' if sample.reactive else 'Non-reactive'
       print(type.ljust(14),end='')
       addedDate = str(sample.entry_date.date())
       print(addedDate.ljust(14),end='')
       if datetime.datetime.now() > sample.expire_date :
            expireIn = 'Expired'
       else :
            expireTime = datetime.datetime.now() - sample.expire_date
            expireIn = f'{expireTime.days} days {expireTime.seconds} Seconds'
       print(str(expireIn).ljust(18),end='')
       print(author.id.ljust(14),end='')
       print()
    print()
    print(f'Total samples {len(samples)}')
    print(f'reactive samples {reactive}')
    print(f'None Reactive samples {non_reactive}')


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
    expire = input('add new samples ,enter new expirey days')
    new_expire = datetime.datetime.now() + datetime.timedelta(expire)
    sample.entry_date = datetime.datetime.now()
    sample.expire_date = new_expire
    session.commit()
    print('Sample succesfully updated...')


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


  def printExpireSamples(user) :
    if user.role == 'LAB' :
       samples = session.query(Sample).filter(Sample.author_id == user.id).all()
       for sample in Samples :
          expire_days = datetime.datetime.utcnow() - sample.expire_date 
