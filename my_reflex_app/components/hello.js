// assets/hello.js
import DataTable from 'datatables.net-react';
import DT from 'datatables.net-dt';
import 'datatables.net-responsive-dt';
import 'datatables.net-select-dt';
import 'datatables.net-dt/css/dataTables.dataTables.min.css';
 
DataTable.use(DT);


export function Hello({ onClick, onBlur, displayText, data, columns }) {
  const handleClick = (event) => {
    const buttonName = event.target.name;
    console.log(`Button clicked: ${buttonName}`);

    if (onClick) {
      onClick(displayText);
    }
  };

  const handleBlur = (event) => {
    const inputName = event.target.name;
    const value = event.target.value;
    console.log(`Input blurred: ${inputName} = ${value}`);

    if (onBlur) {
      onBlur({ input_name: inputName, value }); // Send a dictionary
    }
  };

  const processData = (data) => {
    if (!data) return null;

    return data.map((item, index) => (
      <p key={index}>
        {Object.keys(item).map((key) => (
          <span key={key}>{`${key}: ${item[key]}`} </span>
        ))}
      </p>
    ));
    
  };

  const getAjaxData = () => {
    console.log(onClick);
    console.log(data);
    const myData = [
    {
      "name": "John","age": 30
    }
  ]
  console.log(myData);
  console.log(typeof myData);
    return myData;
  };

  return (
    <div>
      <h1>Hello!</h1>
      <div>{displayText}</div>
      {processData(data)}
      <button name="exampleButton" onClick={handleClick}>
        Click Me
      </button>
      <br />
      <input
        type="text"
        name="exampleInput"
        placeholder="Type something..."
        onBlur={handleBlur}
      />
      <DataTable
            // data={data}
            columns={columns}
            className="display"
            options={{
                responsive: true,
                select: true,
                ajax: function (data, callback, settings) {
                  console.log(data);
                  console.log(settings);
                  callback(getAjaxData());
              }
            }}
            
        >
            <thead>
            <tr>
                <th>Name</th>
                <th>Age</th>
            </tr>
            </thead>
        </DataTable>
    </div>
  );
}