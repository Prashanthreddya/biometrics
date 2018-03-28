# Biometrics
Biometric identification using pinna scan

<h3>Requirements</h3>
<h4>For `insert_mongo.py` :</h4>
You need a `config.py` file in the same folder with the mongodb connection string and path to data.

Example `config.py`:
```
connection_string = 'localhost:port/mydb'
ami_img_dir = './dataset'
```
The filenames have to be in the format `integerID_orientation_otherData.jpg`
Eg: `001_left_ami.jpg`
Only the integer ID and orientation is indexed.
