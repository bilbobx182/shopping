import React from 'react';
import './App.css';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import {Button, TextField} from "@material-ui/core";


class App extends React.Component {


    constructor(props) {
        super(props);
        this.state = {
            search_query: 'Milk',
            result_data: [{'key':1,'description':'hello','shop':'world','price':69}],
        };
    }

    componentDidMount() {
        this.perform_request()
        console.log(this.state.result_data)
    }

    async perform_request() {
          const response = await fetch("http://localhost:8000/products/" + this.state.search_query);
          const data = await response.json();
          console.log(data)
          this.setState({result_data: data});
    }

    updateSearch = (e) => {
        console.log(e.target.value);
        this.setState(() => {
            return {
                search_query: e.target.value
            }
        });
    }

    render() {
        return (
            <div>
                <TextField id="search"
                           value={this.value}
                           onChange={e => {
                               e.persist();
                               this.updateSearch(e)
                           }}
                           label="Standard"/>

                <Button variant="contained" onClick={() => {
                    this.perform_request()
                }}>Search</Button>

                <TableContainer component={Paper}>
                    <Table aria-label="simple table">
                        <TableHead>
                            <TableRow>
                                <TableCell align="left">Item</TableCell>
                                <TableCell align="left">Shop</TableCell>
                                <TableCell align="left">Price</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {this.state.result_data.map((row) => (
                                <TableRow key={row.name}>
                                    <TableCell align="left">{row.description}</TableCell>
                                    <TableCell align="left">{row.shop}</TableCell>
                                    <TableCell align="left">{row.price}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>
        );
    }
}

export default (App);
