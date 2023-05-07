import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-receipes',
  templateUrl: './receipes.component.html',
  styleUrls: ['./receipes.component.scss']
})
export class ReceipesComponent implements OnInit {
  receipeItems = [{"name":"Spaghetti"}, {"name":"Pizza"}, {"name":"Spätzle"}];
  receipeIngredients = [{"name": "Nudeln", "amount": 500, "unit": "gram"}];
  openForm = false;

  constructor(private _http:HttpClient) { }

  ngOnInit(): void {
  }

  loadReceipes(){
    const response = this._http.get('http://localhost:5000/receipes')
    .subscribe((res) =>{
      const resultString = JSON.stringify(res);
      let resultJSON = JSON.parse(resultString);
      this.receipeItems = resultJSON.receipes;
    })
  }

  openFormFunction(){
    this.openForm = true;
  }

  submitReceipe(data:any){
    const response = this._http.post('http://localhost:5000/receipes', {"name":data.form.controls.name.value, "receipe": data.form.controls.receipe.value, "ingredients": this.receipeIngredients}).subscribe(response => {
      this.openForm = false;
      this.loadReceipes();
      data.form.reset()
    })
  }

  submitIngredient(data:any){
    const ingredientToAdd = {"name": data.form.controls.name.value, "amount": data.form.controls.amount.value, "unit": data.form.controls.unit.value};
    this.receipeIngredients.push(ingredientToAdd);
    data.form.reset()
  }
}
