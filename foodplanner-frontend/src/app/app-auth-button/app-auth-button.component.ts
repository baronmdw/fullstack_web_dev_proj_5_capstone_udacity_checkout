import { Component, OnInit } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-app-auth-button',
  templateUrl: './app-auth-button.component.html',
  styleUrls: ['./app-auth-button.component.scss']
})
export class AppAuthButtonComponent implements OnInit {

  constructor(public auth: AuthService) { }

  ngOnInit(): void {
  }

}
