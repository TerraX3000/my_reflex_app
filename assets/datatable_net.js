// assets/datatable_net.js
import { useRef, useEffect } from 'react';
import jszip from 'jszip';
import DataTable from 'datatables.net-react';
import DataTablesCore from 'datatables.net-dt';
import 'datatables.net-buttons-dt';
// import 'datatables.net-buttons/js/buttons.html5.mjs';
import 'datatables.net-responsive-dt';
import 'datatables.net-select-dt';
import 'datatables.net-dt/css/dataTables.dataTables.min.css'
import 'datatables.net-buttons-dt/css/buttons.dataTables.min.css';
 
// DataTablesCore.Buttons.jszip(jszip);

DataTable.use(DataTablesCore);

export function DataTableNet({ data, columns, options, className, slots, isProcessing, onCellValueChanged }) {
    const table = useRef();
    
    useEffect(() => {
        if (table.current) {
            console.log("table ready");
        }
    }, [table]);

    useEffect(() => {
      if (table.current) {
        if (isProcessing) {
          table.current.dt().processing(true);
        } else {
          table.current.dt().processing(false);
        }
      }
    }, [isProcessing]);
  
    const processOptions = (options) => {
      if (!options) return null;
      return options;
    };


    const processSlots = (slots) => {
      console.log("slots", slots);
      if (!slots) return null;
      const basic = {
        2: (data, row) => (
            <Input data={data} row={row} onBlur={onCellValueChanged} />
        ),
        4: (data, row) => (
            <Button data={data} row={row} onClick={onCellValueChanged}>
            </Button>
        )
    }
      return basic;
    };

    return (
      <div>
        <DataTable
          data={data}
          columns={columns}
          ref={table}
          options={{
            ...processOptions(options),
        }}
          className={className}
          slots={processSlots(slots)}
        >
        </DataTable>
      </div>
    );

    function Button({ data, row, onClick }) {
      const handleClick = (event) => {
        const response = {
          value: "Open",
          data: data,
          row: row,
        };
        if (onClick) {
          onClick(response);
        }
      }
      return (
        <button onClick={handleClick}>
          Open
        </button>
      );
    }

  }

  function Input({ data , row, onBlur }) {
    const handleBlur = (event) => {
      const inputName = event.target.name;
      const value = event.target.value;
      const response = {
        name: inputName,
        value: value,
        data: data,
        row: row,
      };
      console.log(response);
      if (onBlur) {
        onBlur(response); // Send a dictionary
      }
    };
  
    return (
      <input
        type="text"
        name="exampleInput"
        onBlur={handleBlur}
      />
    );
  }