import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'foodplanner-frontend';
  responsedata:any;
  constructor(private _http:HttpClient){}

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
