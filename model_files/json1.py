import codecs
import json
import numpy as np

### Change filename accordingly 
in_file="inceptionv4_results_avg_pool.npz"
out_file1="train.json"
out_file2="test.json"

data=np.load(in_file)
train_x=data['X_train'] 
train_y=data['y_train']

test_x=data['X_test']
test_y=data['y_test']

random_names = ["Wanda Ramirez"
    ,"Chris Butler"
    ,"Ruby Allen"
    ,"Ryan Wood"
    ,"Barbara Henderson"
    ,"Diana Nelson"
    ,"Johnny James"
    ,"William Perez"
    ,"Raymond Harris"
    ,"Virginia Lewis"
    ,"Ashley Rivera"
    ,"Jack Taylor"
    ,"Joe Parker"
    ,"Gregory Peterson"
    ,"Anne Bailey"
    ,"Evelyn Perry"
    ,"Theresa Russell"
    ,"Michelle Price"
    ,"Bruce Cooper"
    ,"Catherine Flores"
    ,"Sarah Foster"
    ,"Linda Robinson"
    ,"Jason Green"
    ,"Kathleen Griffin"
    ,"Shawn Campbell"
    ,"Ronald Martinez"
    ,"Jimmy Rodriguez"
    ,"Amy Thomas"
    ,"Cynthia Hernandez"
    ,"Donald Simmons"
    ,"Margaret Gonzales"
    ,"Wayne Hill"
    ,"Joseph Edwards"
    ,"Patricia Bennett"
    ,"Katherine Ross"
    ,"Susan Morgan"
    ,"Frank Howard"
    ,"Phyllis Washington"
    ,"Shirley Jenkins"
    ,"Angela Phillips"
    ,"Louis Thompson"
    ,"Joshua Clark"
    ,"Todd Smith"
    ,"Keith Watson"
    ,"Patrick Wilson"
    ,"Walter Brown"
    ,"Roger Miller"
    ,"Jennifer Kelly"
    ,"Dorothy Williams"
    ,"Carolyn Young"
    ,"Jose Bell"
    ,"Kenneth Barnes"
    ,"Daniel Sanders"
    ,"Helen Coleman"
    ,"Cheryl Murphy"
    ,"Rachel Turner"
    ,"Earl Jackson"
    ,"Irene Johnson"
    ,"Timothy Hughes"
    ,"Deborah Sanchez"
    ,"Mark Richardson"
    ,"Teresa Cox"
    ,"Sandra Torres"
    ,"Sara Garcia"
    ,"Dennis Powell"
    ,"Arthur Gray"
    ,"Sean Adams"
    ,"Martin Diaz"
    ,"Eric Rogers"
    ,"Alan Wright"
    ,"Janet Cook"
    ,"Tina Ward"
    ,"Scott Collins"
    ,"Carlos Bryant"
    ,"Charles Martin"
    ,"Willie Reed"
    ,"Rebecca Stewart"
    ,"Albert Roberts"
    ,"Kevin Jones"
    ,"Ruth Baker"
    ,"Diane Scott"
    ,"Paul Carter"
    ,"Matthew Lee"
    ,"Julie Alexander"
    ,"Julia Lopez"
    ,"David Gonzalez"
    ,"Beverly Walker"
    ,"Gerald Moore"
    ,"Christina King"
    ,"Frances Patterson"
    ,"Pamela Anderson"
    ,"Amanda Morris"
    ,"Steven Mitchell"
    ,"Jeremy Evans"
    ,"Edward White"
    ,"Jacqueline Hall"
    ,"Peter Brooks"
    ,"Larry Davis"
    ,"Emily Long"
    ,"Jane Winchester"]

allocate={}
def train_dump():
    j=0
    with codecs.open(out_file1, "w") as fo1:
        for i in range(len(train_x)):
            dat={}
            dat['sample_class']=train_y[i]
            dat['sample_feature']=train_x[i].tolist()
            if train_y[i] in allocate.keys():
                dat['sample_name']=allocate[train_y[i]]
            else:
                allocate[train_y[i]]=random_names[j]
                j=j+1
                dat['sample_name']=allocate[train_y[i]]
            fo1.write(json.dumps(dat, indent=2)+"\n")

def test_dump():
    with codecs.open(out_file2, "w") as fo2:
        for i in range(len(test_x)):
            dat={}
            dat['sample_class']=test_y[i]
            dat['sample_feature']=test_x[i].tolist()
            dat['sample_name']=allocate[test_y[i]]
            fo2.write(json.dumps(dat, indent=2)+"\n")

train_dump()
test_dump()
