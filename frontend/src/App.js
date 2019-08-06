import React, { Component } from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import Home from './components/Home'
import RedirectComponent from './components/RedirectComponent'
import './App.css';

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <Switch>
          <Route exact path='/' component={Home}/>
          <Route path='/dashboard' component={Dashboard}/>
          <Route path='/login' component={Login}/>
          <Route path='/oauth/redirect' component={RedirectComponent}/>
        </Switch>
      </BrowserRouter>
    );
  }
}

export default App;
