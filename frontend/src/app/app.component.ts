import {AfterViewInit, Component, ViewChild} from '@angular/core';
import {MatSort} from '@angular/material/sort';
import {MatTableDataSource} from '@angular/material/table';
import {SelectionModel} from "@angular/cdk/collections";


const ELEMENT_DATA: any[] = [
  {description: 1, shop: 'Hydrogen', price: 1.0079, symbol: 'H'},
  {description: 2, shop: 'Helium', price: 4.0026, symbol: 'He'},
  {description: 3, shop: 'Lithium', price: 6.941, symbol: 'Li'},
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
  dataSource = new MatTableDataSource(ELEMENT_DATA);
  selectedSource = new MatTableDataSource(SELECTED_DATA);
  search = ''



  @ViewChild(MatSort)
  sort: MatSort = new MatSort;

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
  }

    /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    this.selectedData = this.selection.selected;
    this.selectedSource = new MatTableDataSource<Element>(this.selection.selected);
    return numSelected === numRows;
  }

  getProduct(event:any) {
    console.log("hi")
  }

  updateSearch(event:any) {
    this.search = event.target.value
    this.http.get<any[]>("/courses.json").map(data => _.values(data)).do(console.log);
  }


  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    this.isAllSelected() ?
        this.selection.clear() :
        this.dataSource.data.forEach(row => this.selection.select(row));
  }
}
