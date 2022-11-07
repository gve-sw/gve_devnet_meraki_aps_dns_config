'''Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''




from flask import Flask, render_template, request
import configDNS

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    selected_org=None
    selected_network=None
    if request.method == "POST":
        dns_value=request.form.get('dns')
        selected_org=request.form.get('organizations_select')
        selected_network=request.form.get('network')

        conf=configDNS.configDNS(dns_value,selected_network)
        if conf == True:
            return render_template('home.html', hiddenLinks=True, dropdown_content=configDNS.get_orgs_and_networks(),success=True,selected_elements={'organization':selected_org, 'networkid':selected_network}, names=configDNS.names)
        else:
            return render_template('home.html', hiddenLinks=True, dropdown_content=configDNS.get_orgs_and_networks(),error=True,selected_elements={'organization':selected_org, 'networkid':selected_network})

       
    return render_template('home.html', hiddenLinks=True, dropdown_content=configDNS.get_orgs_and_networks(),selected_elements={'organization':selected_org, 'networkid':selected_network})



if __name__ == '__main__':
    app.run(port=5004,debug=True)