"use strict";

function getRandomNum(upperLimit) {
  return Math.ceil(Math.random() * upperLimit);
}

class Die extends React.Component {
  constructor() {
    super();

    this.state = { value: '?' };  // Set initial value
    this.roll = this.roll.bind(this);
  }

  roll() {
    const rollResult = getRandomNum(this.props.sides);

    // Update state in callback
    this.setState({ value: rollResult });
  }

  render() {
    // Use state in render method to change DOM
    return (
      <button className="die" onClick={this.roll}>
        <i>sides={this.props.sides}</i>
        <b>{this.state.value}</b>
      </button>
    );
  }
}

ReactDOM.render(
  (
    <div>
      <Die sides="4" />
      <Die sides="6" />
      <Die sides="8" />
      <Die sides="10" />
      <Die sides="12" />
      <Die sides="20" />
    </div>
  ),
  document.getElementById('root')
);
