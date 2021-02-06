import React, { useMemo, useState, useEffect } from "react";
import axios from "axios";
import Table from "./components/Table/Ciaran_Table"

//Based off of  https://blog.logrocket.com/complete-guide-building-smart-data-table-react/

function App() {
  const columns = useMemo(
    () => [
      {
        // first group - TV Show
        Header: "Products",
        // First group columns
        columns: [
          {
            Header: "Search",
            accessor: "0"
          },
          {
            Header: "Product",
            accessor: "1"
          },
          {
            Header: "Shop",
            accessor: "2"
          },
          {
            Header: "Price",
            accessor: "3"
          }
        ]
      },
    ],
    []
  );

  const [data, setData] = useState([]);

  // Using useEffect to call the API once mounted and set the data
  useEffect(() => {
    (async () => {
      const result = await axios("http://localhost:8000/products/club orange");
      setData(result.data);
    })();
  }, []);

  return (
    <div className="App">
      <Table columns={columns} data={data} />
    </div>
  );
}

export default App;