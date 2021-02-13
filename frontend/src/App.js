import React from 'react';
import './App.css';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import axios from "axios";
import {Button, TextField} from "@material-ui/core";



class App extends React.Component {


    constructor(props) {
        super(props);
        this.state = {
            search_query: '',
            result_data: []
        };
    }

    componentDidMount() {
        this.perform_request('milk')
        console.log(this.state.result_data)
  }



    perform_request(item) {
        this.setState({apiFilter: item});
        axios("http://localhost:8000/products/" + item).then(({data}) => {
            this.setState({result_data: data })});}


    render() {
        return (
            <div>
                <TextField id="standard-basic" label="Standard"/>
                <Button variant="contained">Search</Button>

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
