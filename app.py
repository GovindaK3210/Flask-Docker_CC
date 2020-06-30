from flask import Flask
app = Flask(__name__)

import socket 
   
     
@app.route('/', methods=['GET'])
def hello():
    roll_no = "i16-0249"
    try: 
        host_name = socket.gethostname() 
     
    except: 
        print("Unable to get Hostname and IP")

    output_return = "Host name: " + host_name + " Rollno: " + roll_no + " Name: Govinda Kumar" 

    return output_return
 
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")

