import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-receipes',
  templateUrl: './receipes.component.html',
  styleUrls: ['./receipes.component.scss']
})
export class ReceipesComponent implements OnInit {
  receipeItems = [{"id": 1, "name":"Spaghetti"}, {"id": 2, "name":"Pizza"}, {"id":3, "name":"Spätzle"}];
  receipeIngredients = [{"name": "Nudeln", "amount": 500, "unit": "gram"}];
  openForm = false;
  showReceipe = false;
  currentReceipe = {"name": "Spaghetti", "description": "fare niente", "id": 0}

  constructor(private _http:HttpClient) { }

  ngOnInit(): void {
    this.loadReceipes();
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
    this.showReceipe = false;
    this.receipeIngredients = [];
  }

  closeCreation(form1:any, form2:any) {
    this.openForm = false;
    this.receipeIngredients = [];
    form1.form.reset();
    form2.form.reset();
  }

  submitReceipe(data:any){
    const response = this._http.post('http://localhost:5000/receipes', {"name":data.form.controls.name.value, "receipe": data.form.controls.receipe.value, "ingredients": this.receipeIngredients}).subscribe(response => {
      this.openForm = false;
      this.loadReceipes();
      data.form.reset()
    })
  }

  openReceipe(receipe:number) {
    const response = this._http.get('http://localhost:5000/receipes/'+receipe)
    .subscribe((res) =>{
      const resultString = JSON.stringify(res);
      let resultJSON = JSON.parse(resultString);
      this.currentReceipe = resultJSON.receipe;
      this.receipeIngredients = resultJSON.ingredients;
      this.showReceipe = true;  
      this.openForm = false;
    })
  }

  closeReceipe(){
    this.openForm = false;
    this.showReceipe = false;
    this.currentReceipe = {"name": "", "description": "", "id":0};
    this.receipeIngredients = [];
  }

  submitIngredient(data:any){
    const ingredientToAdd = {"name": data.form.controls.name.value, "amount": data.form.controls.amount.value, "unit": data.form.controls.unit.value};
    this.receipeIngredients.push(ingredientToAdd);
    data.form.reset()
  }

  deleteReceipe(){
    const response = this._http.delete('http://localhost:5000/receipes/'+this.currentReceipe.id)
    .subscribe((res)=> {
      this.closeReceipe();
      this.loadReceipes();
    })
  }

  dropIngredient(name:String) {
      this.receipeIngredients.forEach((element, index) => {
        if (element.name == name) {
          console.log("element found")
          this.receipeIngredients.splice(index,1);
        }
      })
  }

  editReceipe(){
    this.showReceipe = false;
    this.openForm = true;

  }
}
