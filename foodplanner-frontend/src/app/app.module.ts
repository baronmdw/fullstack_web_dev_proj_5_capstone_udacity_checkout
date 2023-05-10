import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { MatToolbarModule   } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { MatIcon, MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';
import { GrocerylistComponent } from './grocerylist/grocerylist.component';
import { WeekplanComponent } from './weekplan/weekplan.component';
import { ReceipesComponent } from './receipes/receipes.component';
import { MatCardModule } from '@angular/material/card'; 

import { AuthModule } from '@auth0/auth0-angular';
import { AppAuthButtonComponent } from './app-auth-button/app-auth-button.component';


@NgModule({
  declarations: [
    AppComponent,
    GrocerylistComponent,
    WeekplanComponent,
    ReceipesComponent,
    AppAuthButtonComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatButtonModule,
    MatToolbarModule,
    MatListModule,
    MatIconModule,
    MatInputModule,
    FormsModule,
    MatCardModule,
    AuthModule.forRoot({
      domain: 'fsnd-mdw.eu.auth0.com',
      clientId: 'wMgoDyWEm8SfKtlSU3RzApCjpbYeL9Dt',
      authorizationParams: {
        redirect_uri: window.location.origin
      }
    }),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
