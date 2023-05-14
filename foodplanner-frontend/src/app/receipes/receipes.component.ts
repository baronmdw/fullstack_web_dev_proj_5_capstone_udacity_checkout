import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../auth.service';


@Component({
  selector: 'app-receipes',
  templateUrl: './receipes.component.html',
  styleUrls: ['./receipes.component.scss']
})
export class ReceipesComponent implements OnInit {
  // component variables storing information or status
  receipeItems = [{"id": 1, "name":"Spaghetti"}, {"id": 2, "name":"Pizza"}, {"id":3, "name":"Spätzle"}];
  receipeIngredients = [{"name": "Nudeln", "amount": 500, "unit": "gram"}];
  openForm = false;
  showReceipe = false;
  currentReceipe = {"name": "Spaghetti", "description": "fare niente", "id": 0};
  editReceipeMode = false;
  loginURL: string;
  // Form variables
  receipeName = "";
  receipeDescription = "";

  constructor(private _http:HttpClient, public auth: AuthService) {
    this.loginURL = auth.build_login_link('');
   }

  ngOnInit(): void {
    this.loadReceipes();
  }

  // This function loads the receipes by addressing the get-endpoint for reading all receipes and putting the result to the respective variable
  loadReceipes(){
    const response = this._http.get('http://localhost:5000/receipes')
    .subscribe((res) =>{
      const resultString = JSON.stringify(res);
      let resultJSON = JSON.parse(resultString);
      this.receipeItems = resultJSON.receipes;
    })
  }

  // This function opens the form template and closes the receipe details, the ingredientslist is emptied to enable a new form.
  openFormFunction(){
    this.openForm = true;
    this.showReceipe = false;
    this.receipeIngredients = [];
  }

  // This function cancels the creation process of a new receipe item by closing the form and resetting the variables and forms
  closeCreation(form1:any, form2:any) {
    this.openForm = false;
    this.receipeIngredients = [];
    form1.form.reset();
    form2.form.reset();
  }

  // This function submits the receipe to create a new one or update an existing one depending on the editReceipeMode flag
  submitReceipe(data:any){
    if (!this.editReceipeMode){
      // create new receipe
      const response = this._http.post('http://localhost:5000/receipes', {"name":data.form.controls.name.value, "receipe": data.form.controls.receipe.value, "ingredients": this.receipeIngredients}).subscribe(response => {
        this.openForm = false;
        this.loadReceipes();
        data.form.reset()
      });
    } else {
      // update existing receipe
      const response = this._http.patch('http://localhost:5000/receipes/'+this.currentReceipe.id, {"name":data.form.controls.name.value, "receipe": data.form.controls.receipe.value, "ingredients": this.receipeIngredients}).subscribe(response => {
        this.openForm = false;
        this.editReceipeMode = false;
        this.loadReceipes();
        data.form.reset() 
      });
    }
  }

  // this function calls the api to get the details of a receipe, saves them to the corresponding variables, closes the input form and opens the receipe form
  openReceipe(receipe:number) {
    const response = this._http.get('http://localhost:5000/receipes/'+receipe)
    .subscribe((res) =>{
      const resultString = JSON.stringify(res);
      let resultJSON = JSON.parse(resultString);
      this.currentReceipe = resultJSON.receipe;
      this.receipeIngredients = resultJSON.ingredients;
      this.openForm = false;
      this.showReceipe = true;  
    })
  }

  // this function closes the receipe view and resets the corresponding variables
  closeReceipe(){
    this.openForm = false;
    this.showReceipe = false;
    this.currentReceipe = {"name": "", "description": "", "id":0};
    this.receipeIngredients = [];
  }

  // this function adds ingredients to the CLIENT list of ingredients, it doesn't save it to the backend
  submitIngredient(data:any){
    const ingredientToAdd = {"name": data.form.controls.name.value, "amount": data.form.controls.amount.value, "unit": data.form.controls.unit.value};
    this.receipeIngredients.push(ingredientToAdd);
    data.form.reset()
  }

  // this function calls the api to delete a specific receipe
  deleteReceipe(){
    const response = this._http.delete('http://localhost:5000/receipes/'+this.currentReceipe.id)
    .subscribe((res)=> {
      this.closeReceipe();
      this.loadReceipes();
    })
  }

  // this fucntion drops an ingredient of the CLIENTs ingredientlist, not from the backend
  dropIngredient(name:String) {
      this.receipeIngredients.forEach((element, index) => {
        if (element.name == name) {
          console.log("element found")
          this.receipeIngredients.splice(index,1);
        }
      })
  }

  // this fucntion starts the editing mode for a receipe
  editReceipe(){
    this.showReceipe = false;
    this.openForm = true;
    this.editReceipeMode = true;
    this.receipeName = this.currentReceipe.name;
    this.receipeDescription = this.currentReceipe.description;
  }

}
