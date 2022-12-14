import os
import datetime
from zifoDatabase import session,Sample

class ZifoUser :


  def clear(self) :
    clear_val = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear_val)


  def addSamples(self,author) :
     self.clear()
     if author.role == 'LAB' :
       print('you dont have rights to do add samples... ')
       return
     type = bool(int(input('enter type of reactive 1 => reactive,0 => Non reactive ')))
     expire_days = int(input('Enter no of days to expire '))
     new_samples = Sample(
             reactive = type,
             entry_date = datetime.date.today(),
             expire_date = datetime.datetime.utcnow() + datetime.timedelta(days=expire_days),
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
    print('Id     Name     Type     addedDate   Expirein     author')
    samples = session.query(Sample).filter(Sample.author.id == author.id ).all()
    reactive = 0;non_reactive = 0
    for sample in samples :
       if sample.type == True :
         reactive += 1
       else:
         non_reactive += 1
       print(sample.id.ljust(8),end='')
       print(sample.name.ljust(10),end='')
       type =  'Reactive' if sample.type else 'Non-reactive'
       print(type.ljust(9),end='')
       addedDate = str(sample.entry_date)
       print(addedDate.ljust(9),end='')
       if datetime.datetime.utcnow() > sample.expire_date :
         expireIn = 'Expired'
       else:
         expireIn = datetime.datetime.utcnow() - sample.expire_date
       print(expireIn.ljust(10),end='')
       print(author.id.lust(10),end='')
       print()
    print()
    print(f'your Total samples {len(samples)}')
    print(f'reactive samples {reactive}')
    print(f'None Reactive samples {non_reactive}')


  def getAllSamples(self,author):
    self.clear()
    print('Id     Name     Type     addedDate   Expirein     author')
    samples = session.query(Sample).filter(sample.author.id == author.id ).all()
    reactive = 0;non_reactive = 0
    for sample in samples :
       if sample.type == True :
         reactive += 1
       else:
         non_reactive += 1
       print(sample.id.ljust(8),end='')
       print(sample.name.ljust(10),end='')
       type =  'Reactive' if sample.type else 'Non-reactive'
       print(type.ljust(9),end='')
       addedDate = str(sample.entry_date)
       print(addedDate.ljust(9),end='')
       if datetime.datetime.utcnow() > sample.expire_date :
            expireIn = 'Expired'
       else :
         expireIn = datetime.datetime.utcnow() - sample.expire_date
       print(expireIn.ljust(10),end='')
       print(author.id.lust(10),end='')
       print()
    print()
    print(f'Total samples {len(samples)}')
    print(f'reactive samples {reactive}')
    print(f'None Reactive samples {non_reactive}')


  def updateSamples(self,author) :
    self.clear()
    if author.role == 'LAB' :
      print('you dont have permissions to update the samples...')
      return
    sample_id = int(input('Enter sample id '))
    sample = session.query(Sample).filter(Sample.id == sample_id).first()
    if sample is None :
      print('Inavlid sample Id...')
      return
    if sample.author.id != author.id :
      print('you dont have permissions to update another person samples')
      return
    expire = input('add new samples ,enter new expirey days')
    new_expire = datetime.datetime.utcnow() +datetime.timedelta(expire)
    sample.entry_date = datetime.date.today()
    sample.expire_date = new_expire
    session.commit()
    print('Sample succesfully updated...')


  def deleteSample(self,author):
    self.clear()
    if author.role == 'LAB' :
      print('you dont have permissions to delete the samples...')
      return
    sample_id = int(input('Enter Sample Id '))
    sample = session.query(Sample).filter(Sample.id == sample_id).first()
    if sample is None :
      print('Inavalid sample Id...')
      return
    if sample.author.id != author.id :
      print('you dont have permissions to delete another person samples ...')
      return
    session.delete(sample)
    session.commit()
    print('Sample deleted Successfully...')
