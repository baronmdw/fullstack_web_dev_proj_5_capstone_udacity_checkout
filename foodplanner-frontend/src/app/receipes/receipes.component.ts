import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-receipes',
  templateUrl: './receipes.component.html',
  styleUrls: ['./receipes.component.scss']
})
export class ReceipesComponent implements OnInit {
  receipeItems = ["Spaghetti", "Pizza", "Spätzle"];

  constructor() { }

  ngOnInit(): void {
  }

}
