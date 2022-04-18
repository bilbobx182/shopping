import {AfterViewInit, Component, ViewChild,ChangeDetectorRef} from '@angular/core';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import {SelectionModel} from "@angular/cdk/collections";
import {MAT_FORM_FIELD, MatFormField, MatFormFieldControl} from '@angular/material/form-field';
import { HttpClient } from '@angular/common/http';

const ELEMENT_DATA: any[] = [
  {description: 1, shop: 'TESCO', price: 1},
];

const SELECTED_DATA: any[] = [
];

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewInit {
  title = 'Grocery Gauge';
  selection = new SelectionModel<any>(true, []);
  selectedData : any[] = this.selection.selected
  displayedColumns: string[] = ['select','description','shop', 'price'];
  selectedColums: string[] = ['description','shop', 'price'];
  data:any[] = [];

  dataSource = new MatTableDataSource(ELEMENT_DATA);
  search = ''

  @ViewChild(MatSort)
  sort: MatSort = new MatSort;
  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

  constructor(private httpClient: HttpClient,private changeDetectorRefs: ChangeDetectorRef) { }



  getProduct(event:any) {
     this.httpClient.get<any[]>(`http://0.0.0.0:8000/products/${this.search}`)
           .subscribe(data => {
               this.data= data;
                 this.dataSource = new MatTableDataSource(this.data);
                 this.dataSource.sort = this.sort;
                 this.refresh();
           }
  );
  }

  updateSearch(event:any) {
    this.search = event.target.value
    console.log(this.search)
  }

  refresh() {
  this.changeDetectorRefs.detectChanges();
  }
}
