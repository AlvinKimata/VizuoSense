import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:provider/provider.dart';

//import '/custom_code/actions/index.dart' as actions;
import 'start_model.dart';
export 'start_model.dart';

class StartWidget extends StatefulWidget {
  const StartWidget({Key? key}) : super(key: key);

  @override
  State<StartWidget> createState() => _StartWidgetState();
}

class _StartWidgetState extends State<StartWidget> {
  late StartModel _model;

  final scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _model = createModel(context, () => StartModel());

    _model.textController ??= TextEditingController();
    _model.textFieldFocusNode ??= FocusNode();

    WidgetsBinding.instance!.addPostFrameCallback((_) => setState(() {}));
  }

  @override
  void dispose() {
    _model.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (Theme.of(context).platform == TargetPlatform.iOS) {
      SystemChrome.setSystemUIOverlayStyle(
        SystemUiOverlayStyle(
          statusBarBrightness: Theme.of(context).brightness,
          systemStatusBarContrastEnforced: true,
        ),
      );
    }

    return GestureDetector(
      onTap: () => _model.unfocusNode.canRequestFocus
          ? FocusScope.of(context).requestFocus(_model.unfocusNode)
          : FocusScope.of(context).unfocus(),
      child: Scaffold(
        key: scaffoldKey,
        backgroundColor: Theme.of(context).primaryColor,
        body: SafeArea(
          top: true,
          child: Column(
            mainAxisSize: MainAxisSize.max,
            children: [
              Column(
                mainAxisSize: MainAxisSize.max,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Container(
                    decoration: BoxDecoration(),
                    child: Column(
                      mainAxisSize: MainAxisSize.max,
                      children: [
                        Container(
                          width: double.infinity,
                          height: 199,
                          decoration: BoxDecoration(
                            color: Theme.of(context).primaryColor,
                          ),
                        ),
                        Padding(
                          padding: EdgeInsetsDirectional.fromSTEB(0, 10, 0, 0),
                          child: Row(
                            mainAxisSize: MainAxisSize.max,
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Padding(
                                padding:
                                    EdgeInsetsDirectional.fromSTEB(30, 0, 0, 0),
                                child: ElevatedButton(
                                  onPressed: () async {
                                    //await actions.startcamera();
                                  },
                                  style: ElevatedButton.styleFrom(
                                    primary: Theme.of(context).primaryColor,
                                    padding: EdgeInsets.zero,
                                    elevation: 0,
                                  ),
                                  child: FaIcon(
                                    FontAwesomeIcons.camera,
                                    color: Theme.of(context).accentColor,
                                  ),
                                ),
                              ),
                              Padding(
                                padding:
                                    EdgeInsetsDirectional.fromSTEB(0, 0, 30, 0),
                                child: ElevatedButton(
                                  onPressed: () async {
                                    // await actions.startcamera();
                                  },
                                  style: ElevatedButton.styleFrom(
                                    primary: Theme.of(context).primaryColor,
                                    padding: EdgeInsets.zero,
                                    elevation: 0,
                                  ),
                                  child: Icon(
                                    Icons.stop_circle,
                                    color: Theme.of(context).errorColor,
                                    size: 15,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  Container(
                    height: 387,
                    child: Stack(
                      children: [
                        Column(
                          mainAxisSize: MainAxisSize.max,
                          children: [
                            Container(
                              width: 400,
                              height: 321,
                              decoration: BoxDecoration(
                                color: Theme.of(context).backgroundColor,
                              ),
                              child: Padding(
                                padding: EdgeInsetsDirectional.fromSTEB(
                                    25, 25, 25, 0),
                                child: Text(
                                  'model Text output... ',
                                  style: Theme.of(context).textTheme.bodyText1,
                                ),
                              ),
                            ),
                            Padding(
                              padding:
                                  EdgeInsetsDirectional.fromSTEB(0, 20, 0, 0),
                              child: ElevatedButton(
                                onPressed: () {
                                  print('Button pressed ...');
                                },
                                style: ElevatedButton.styleFrom(
                                  primary: Theme.of(context).primaryColor,
                                  padding: EdgeInsetsDirectional.fromSTEB(
                                      24, 0, 24, 0),
                                  elevation: 3,
                                  shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(8),
                                  ),
                                ),
                                child: Text(
                                  'play',
                                  style: Theme.of(context).textTheme.subtitle1,
                                ),
                              ),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              Row(
                mainAxisSize: MainAxisSize.max,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Expanded(
                    child: Padding(
                      padding: EdgeInsetsDirectional.fromSTEB(8, 0, 16, 0),
                      child: TextFormField(
                        controller: _model.textController,
                        focusNode: _model.textFieldFocusNode,
                        autofocus: true,
                        obscureText: false,
                        decoration: InputDecoration(
                          labelText: 'Enter Prompt',
                          labelStyle: Theme.of(context).textTheme.subtitle1,
                          hintText: 'prompt...',
                          hintStyle: Theme.of(context).textTheme.subtitle1,
                          enabledBorder: OutlineInputBorder(
                            borderSide: BorderSide(
                              color: Theme.of(context).accentColor,
                              width: 2,
                            ),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          focusedBorder: OutlineInputBorder(
                            borderSide: BorderSide(
                              color: Theme.of(context).primaryColor,
                              width: 2,
                            ),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          errorBorder: OutlineInputBorder(
                            borderSide: BorderSide(
                              color: Theme.of(context).errorColor,
                              width: 2,
                            ),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          focusedErrorBorder: OutlineInputBorder(
                            borderSide: BorderSide(
                              color: Theme.of(context).errorColor,
                              width: 2,
                            ),
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                        style: Theme.of(context).textTheme.bodyText1,
                        maxLines: 2,
                        validator:
                            _model.textControllerValidator.asValidator(context),
                      ),
                    ),
                  ),
                  Padding(
                    padding: EdgeInsetsDirectional.fromSTEB(0, 0, 5, 0),
                    child: IconButton(
                      color:
                          Theme.of(context).primaryTextTheme.bodyText1!.color,
                      icon: Icon(
                        Icons.send_outlined,
                        size: 24,
                      ),
                      onPressed: () {
                        print('IconButton pressed ...');
                      },
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
