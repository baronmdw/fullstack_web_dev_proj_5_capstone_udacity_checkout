import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-weekplan',
  templateUrl: './weekplan.component.html',
  styleUrls: ['./weekplan.component.scss']
})

export class WeekplanComponent implements OnInit {

  weekPlan = [{"day": "Montag", "lunch": "Eier", "dinner": "Spaghetti"},{"day": "Dienstag", "dinner": "Pizza"}];

  constructor() { }

  ngOnInit(): void {
  }

}
