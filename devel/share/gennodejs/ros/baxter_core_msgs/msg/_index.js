
"use strict";

let DigitalOutputCommand = require('./DigitalOutputCommand.js');
let CameraSettings = require('./CameraSettings.js');
let DigitalIOStates = require('./DigitalIOStates.js');
let CameraControl = require('./CameraControl.js');
let EndEffectorState = require('./EndEffectorState.js');
let NavigatorStates = require('./NavigatorStates.js');
let AssemblyState = require('./AssemblyState.js');
let AnalogOutputCommand = require('./AnalogOutputCommand.js');
let CollisionAvoidanceState = require('./CollisionAvoidanceState.js');
let AssemblyStates = require('./AssemblyStates.js');
let AnalogIOState = require('./AnalogIOState.js');
let AnalogIOStates = require('./AnalogIOStates.js');
let EndpointState = require('./EndpointState.js');
let NavigatorState = require('./NavigatorState.js');
let HeadPanCommand = require('./HeadPanCommand.js');
let URDFConfiguration = require('./URDFConfiguration.js');
let SEAJointState = require('./SEAJointState.js');
let DigitalIOState = require('./DigitalIOState.js');
let RobustControllerStatus = require('./RobustControllerStatus.js');
let JointCommand = require('./JointCommand.js');
let HeadState = require('./HeadState.js');
let EndEffectorCommand = require('./EndEffectorCommand.js');
let CollisionDetectionState = require('./CollisionDetectionState.js');
let EndEffectorProperties = require('./EndEffectorProperties.js');
let EndpointStates = require('./EndpointStates.js');

module.exports = {
  DigitalOutputCommand: DigitalOutputCommand,
  CameraSettings: CameraSettings,
  DigitalIOStates: DigitalIOStates,
  CameraControl: CameraControl,
  EndEffectorState: EndEffectorState,
  NavigatorStates: NavigatorStates,
  AssemblyState: AssemblyState,
  AnalogOutputCommand: AnalogOutputCommand,
  CollisionAvoidanceState: CollisionAvoidanceState,
  AssemblyStates: AssemblyStates,
  AnalogIOState: AnalogIOState,
  AnalogIOStates: AnalogIOStates,
  EndpointState: EndpointState,
  NavigatorState: NavigatorState,
  HeadPanCommand: HeadPanCommand,
  URDFConfiguration: URDFConfiguration,
  SEAJointState: SEAJointState,
  DigitalIOState: DigitalIOState,
  RobustControllerStatus: RobustControllerStatus,
  JointCommand: JointCommand,
  HeadState: HeadState,
  EndEffectorCommand: EndEffectorCommand,
  CollisionDetectionState: CollisionDetectionState,
  EndEffectorProperties: EndEffectorProperties,
  EndpointStates: EndpointStates,
};
