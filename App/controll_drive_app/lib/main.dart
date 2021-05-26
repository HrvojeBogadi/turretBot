import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:math';

import 'package:control_pad/control_pad.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  SystemChrome.setPreferredOrientations([DeviceOrientation.landscapeRight])
    .then((value) => runApp(MyApp()));
}

class MyApp extends StatelessWidget {
  bool isInTurretMode = false;
  void onJoystickEvent(double angle, double distance){
    double x, y;

    y = distance * cos(angle/(180) * pi);
    x = distance * sin(angle/(180) * pi);

    print("X Cartesian: $x, Y Cartesian: $y");
    //TODO : Send coordinates to RPi
  }

  void onButtonPress(){
    if (!isInTurretMode){
      print("Turret Mode Engaged!");
      isInTurretMode=true;
    }else{
      print("Turret Mode Disengaged!");
      isInTurretMode=false;
    }


    //TODO : Send Turret Mode Changed to RPi
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Stack(
          fit: StackFit.expand,
          children: <Widget>[
            Container(
              alignment: AlignmentDirectional.bottomEnd,
              child: Container(
                height: 125,
                width: 200,
                margin: EdgeInsets.only(right: 25, bottom: 25),
                child: JoystickView(
                  size: 125,
                  showArrows: false,
                  innerCircleColor: Colors.blueAccent,
                  backgroundColor: Colors.black87,
                  onDirectionChanged: onJoystickEvent
                ),
              ),
            ),

            Container(
              alignment: AlignmentDirectional.bottomStart,
              margin: EdgeInsets.only(left: 100, bottom: 50),
              child: ElevatedButton(
                onPressed: onButtonPress,
                child: Text(
                  "Turret Mode"
                ),
                style: ElevatedButton.styleFrom(
                  primary: Colors.blueAccent
                ),
              ),
            )
          ],
        ),
    );
  }

}