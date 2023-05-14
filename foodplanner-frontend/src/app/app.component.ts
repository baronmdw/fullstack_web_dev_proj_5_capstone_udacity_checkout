import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Platform } from '@ionic/angular';

import { AuthService } from './auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'foodplanner-frontend';
  responsedata:any;
  constructor(
    private _http:HttpClient,
    private auth: AuthService,
    private platform: Platform,
    ){
      this.initializeApp();
    }


  initializeApp() {
    this.platform.ready().then(() => {
      // this.statusBar.styleDefault();
      // this.splashScreen.hide();

      // Perform required auth actions
      this.auth.load_jwts();
      this.auth.check_token_fragment();
    });
  }
  connectionTest() {
    const response = this._http.get('http://localhost:5000/')
    .subscribe(res =>{
      this.responsedata = res;
      const divToChange = document.getElementById("test");
      if (divToChange){
        divToChange.textContent = this.responsedata[0]["id"] + " " + this.responsedata[0]["text"];
      }
    })
  }
}
