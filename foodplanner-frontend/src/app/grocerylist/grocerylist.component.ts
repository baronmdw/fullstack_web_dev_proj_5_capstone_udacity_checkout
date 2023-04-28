import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-grocerylist',
  templateUrl: './grocerylist.component.html',
  styleUrls: ['./grocerylist.component.scss']
})
export class GrocerylistComponent implements OnInit {
  groceryItems = ["Äpfel", "Birnen", "Bananen", "Dadda"]

  constructor() { }

  ngOnInit(): void {
  }

}
