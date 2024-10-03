classdef EasyEqualizer151 < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        UIFigure          matlab.ui.Figure
        AudioFileLabel    matlab.ui.control.Label
        AudioFileEdit     matlab.ui.control.EditField
        BrowseButton      matlab.ui.control.Button
        OriginalAxes      matlab.ui.control.UIAxes
        EqualizedAxes     matlab.ui.control.UIAxes
        Gain1Label        matlab.ui.control.Label
        Gain1Slider       matlab.ui.control.Slider
        Gain1EditField    matlab.ui.control.EditField
        Gain2Label        matlab.ui.control.Label
        Gain2Slider       matlab.ui.control.Slider
        Gain2EditField    matlab.ui.control.EditField
        Gain3Label        matlab.ui.control.Label
        Gain3Slider       matlab.ui.control.Slider
        Gain3EditField    matlab.ui.control.EditField
        Gain4Label        matlab.ui.control.Label
        Gain4Slider       matlab.ui.control.Slider
        Gain4EditField    matlab.ui.control.EditField
        Gain5Label        matlab.ui.control.Label
        Gain5Slider       matlab.ui.control.Slider
        Gain5EditField    matlab.ui.control.EditField
        Gain6Label        matlab.ui.control.Label
        Gain6Slider       matlab.ui.control.Slider
        Gain6EditField    matlab.ui.control.EditField
        Gain7Label        matlab.ui.control.Label
        Gain7Slider       matlab.ui.control.Slider
        Gain7EditField    matlab.ui.control.EditField
        Gain8Label        matlab.ui.control.Label
        Gain8Slider       matlab.ui.control.Slider
        Gain8EditField    matlab.ui.control.EditField
        Gain9Label        matlab.ui.control.Label
        Gain9Slider       matlab.ui.control.Slider
        Gain9EditField    matlab.ui.control.EditField
        Gain10Label       matlab.ui.control.Label
        Gain10Slider      matlab.ui.control.Slider
        Gain10EditField    matlab.ui.control.EditField
        ProcessButton     matlab.ui.control.Button
        EQButton          matlab.ui.control.Button
        Play1Button       matlab.ui.control.Button
        Play2Button       matlab.ui.control.Button
    end

    % App components properties that correspond to app logic and data
    properties (Access = private)
        flag1 = 0
        flag2 = 0
        Fs
        y
        y_eq
        B
        A
        player1
        player2
    end

    % App components methods
    methods (Access = private)

        % Audio file browser callback function
        function BrowseButtonPushed(app, ~)

            % Browse audio file
            [filename, path] = uigetfile({'*.wav','Waveform Audio File Format (*.wav)'},'Select audio file');
            if isequal(filename,0) || isequal(path,0)
                return;
            end

            % Update audio file label and load audio file
            app.AudioFileEdit.Value = fullfile(path,filename);
            app.flag1 = 1;
            app.flag2 = 0;
            [app.y, app.Fs] = audioread(app.AudioFileEdit.Value);

            % Update original audio plot
            plot(app.OriginalAxes, (1:length(app.y))/app.Fs, app.y, 'b');
            xlabel(app.OriginalAxes, 'Time (s)');
            ylabel(app.OriginalAxes, 'Amplitude');
            title(app.OriginalAxes, 'Original Audio - Time Domain');

            % Update equalized audio plot
            cla(app.EqualizedAxes);
            xlabel(app.EqualizedAxes, 'Time (s)');
            ylabel(app.EqualizedAxes, 'Amplitude');
            title(app.EqualizedAxes, 'Equalized Audio - Time Domain');

             % Reset gain sliders
                    app.Gain1Slider.Value = 1;
                    app.Gain2Slider.Value = 1;
                    app.Gain3Slider.Value = 1;
                    app.Gain4Slider.Value = 1;
                    app.Gain5Slider.Value = 1;
                    app.Gain6Slider.Value = 1;
                    app.Gain7Slider.Value = 1;
                    app.Gain8Slider.Value = 1;
                    app.Gain9Slider.Value = 1;
                    app.Gain10Slider.Value = 1;

            % Compute filter coefficients
            fc = [30 60 120 240 480 960 1920 3840 7680 15360];
            app.B = cell(length(fc), 1);
            app.A = cell(length(fc), 1);
            for i = 1:length(fc)
                [app.B{i}, app.A{i}] = butter(2, [fc(i)*(2^(-1/6)), fc(i)*(2^(1/6))]/(app.Fs/2), 'bandpass');
            end

        end

    end
    
    % App creation and deletion methods
    methods (Access = public)
    
        % Construct app
        function app = EasyEqualizer151
    
            % Create UIFigure and components
            app.UIFigure = uifigure;
            app.UIFigure.Position = [0 0 1200 960];
            app.UIFigure.Name = 'EasyEqualizer151';
            app.UIFigure.DeleteFcn = createCallbackFcn(app, @delete);
    
            % Create AudioFileLabel
            app.AudioFileLabel = uilabel(app.UIFigure);
            app.AudioFileLabel.HorizontalAlignment = 'right';
            app.AudioFileLabel.Position = [80 900 60 30];
            app.AudioFileLabel.Text = 'Audio File';
    
            % Create AudioFileEdit
            app.AudioFileEdit = uieditfield(app.UIFigure, 'text');
            app.AudioFileEdit.HorizontalAlignment = 'left';
            app.AudioFileEdit.Position = [170 900 750 30];
    
            % Create BrowseButton
            app.BrowseButton = uibutton(app.UIFigure, 'push');
            app.BrowseButton.ButtonPushedFcn = createCallbackFcn(app, @BrowseButtonPushed);
            app.BrowseButton.Position = [940 900 60 30];
            app.BrowseButton.Text = 'Browse';

            % Create OriginalAxes
            app.OriginalAxes = uiaxes(app.UIFigure);
            app.OriginalAxes.Position = [80 600 400 250];
            
            % Create EqualizedAxes
            app.EqualizedAxes = uiaxes(app.UIFigure);
            app.EqualizedAxes.Position = [600 600 400 250];
    
            % Create Gain1Slider
            app.Gain1Slider = uislider(app.UIFigure);
            app.Gain1Slider.Limits = [-12 12];
            app.Gain1Slider.MajorTicks = [-12 -9 -6 -3 0 3 6 9 12];
            app.Gain1Slider.Position = [175 525 300 3];
            app.Gain1Slider.Value = 1;

            % Create Gain1EditField
            app.Gain1EditField = uieditfield(app.UIFigure, 'text');
            app.Gain1EditField.Value = '1';
            app.Gain1EditField.Position = [500 500 50 30];
            app.Gain1Slider.ValueChangedFcn = @(~,~) updateGainValue(app,app.Gain1EditField,app.Gain1Slider);
            app.Gain1EditField.ValueChangedFcn = @(~,~) updateGainSlider(app,app.Gain1Slider,app.Gain1EditField);

            % Create Gain2Slider
            app.Gain2Slider = uislider(app.UIFigure);
            app.Gain2Slider.Limits = [-12 12];
            app.Gain2Slider.MajorTicks = [-12 -9 -6 -3 0 3 6 9 12];
            app.Gain2Slider.Position = [175 475 300 3];
            app.Gain2Slider.Value = 1;
            
            % Create Gain2EditField
            app.Gain2EditField = uieditfield(app.UIFigure, 'text');
            app.Gain2EditField.Value = '1';
            app.Gain2EditField.Position = [500 450 50 30];
            app.Gain2Slider.ValueChangedFcn = @(~,~) updateGainValue(app,app.Gain2EditField,app.Gain2Slider);
            app.Gain2EditField.ValueChangedFcn = @(~,~) updateGainSlider(app,app.Gain2Slider,app.Gain2EditField);

            % Create Gain3Slider
            app.Gain3Slider = uislider(app.UIFigure);
            app.Gain3Slider.Limits = [-12 12];
            app.Gain3Slider.MajorTicks = [-12 -9 -6 -3 0 3 6 9 12];
            app.Gain3Slider.Position = [175 425 300 3];
            app.Gain3Slider.Value = 1;
            
            % Create Gain3EditField
            app.Gain3EditField = uieditfield(app.UIFigure, 'text');
            app.Gain3EditField.Value = '1';
            app.Gain3EditField.Position = [500 400 50 30];
            app.Gain3Slider.ValueChangedFcn = @(~,~) updateGainValue(app,app.Gain3EditField,app.Gain3Slider);
            app.Gain3EditField.ValueChangedFcn = @(~,~) updateGainSlider(app,app.Gain3Slider,app.Gain3EditField);

            % Create Gain4Slider
            app.Gain4Slider = uislider(app.UIFigure);
            app.Gain4Slider.Limits = [-12 12];
            app.Gain4Slider.MajorTicks = [-12 -9 -6 -3 0 3 6 9 12];
            app.Gain4Slider.Position = [175 375 300 3];
            app.Gain4Slider.Value = 1;
            
            % Create Gain4EditField
            app.Gain4EditField = uieditfield(app.UIFigure, 'text');
            app.Gain4EditField.Value = '1';
            app.Gain4EditField.Position = [500 350 50 30];
            app.Gain4Slider.ValueChangedFcn = @(~,~) updateGainValue(app,app.Gain4EditField,app.Gain4Slider);
            app.Gain4EditField.ValueChangedFcn = @(~,~) updateGainSlider(app,app.Gain4Slider,app.Gain4EditField);

            % Create Gain5Slider
            app.Gain5Slider = uislider(app.UIFigure);
            app.Gain5Slider.Limits = [-12 12];
            app.Gain5Slider.MajorTicks = [-12 -9 -6 -3 0 3 6 9 12];
            app.Gain5Slider.Position = [175 325 300 3];
            app.Gain5Slider.Value = 1;
                       
            % Create Gain5EditField
            app.Gain5EditField = uieditfield(app.UIFigure, 'text');
            app.Gain5EditField.Value = '1';
            app.Gain5EditField.Position = [500 300 50 30];
            app.Gain5Slider.ValueChangedFcn = @(~,~) updateGainValue(app,app.Gain5EditField,app.Gain5Slider);
            app.Gain5EditField.ValueChangedFcn = @(~,~) updateGainSlider(app,app.Gain5Slider,app.Gain5EditField);

            % Create Gain6Slider
            app.Gain6Slider = uislider(app.UIFigure);
            app.Gain6Slider.Limits = [-12 12];
            app.Gain6Slider.MajorTicks = [-12 -9 -6 -3 0 3 6 9 12];
            app.Gain6Slider.Position = [695 525 300 3];
            app.Gain6Slider.Value = 1;
            
            % Create Gain6EditField
            app.Gain6EditField = uieditfield(app.UIFigure, 'text');
            app.Gain6EditField.Value = '1';
            app.Gain6EditField.Position = [1020 500 50 30];
            app.Gain6Slider.ValueChangedFcn = @(~,~) updateGainValue(app,app.Gain6EditField,app.Gain6Slider);
            app.Gain6EditField.ValueChangedFcn = @(~,~) updateGainSlider(app,app.Gain6Slider,app.Gain6EditField);

            % Create Gain7Slider
            app.Gain7Slider = uislider(app.UIFigure);
            app.Gain7Slider.Limits = [-12 12];
            app.Gain7Slider.MajorTicks = [-12 -9 -6 -3 0 3 6 9 12];
            app.Gain7Slider.Position = [695 475 300 3];
            app.Gain7Slider.Value = 1;

            % Create Gain7EditField
            app.Gain7EditField = uieditfield(app.UIFigure, 'text');
            app.Gain7EditField.Value = '1';
            app.Gain7EditField.Position = [1020 450 50 30];
            app.Gain7Slider.ValueChangedFcn = @(~,~) updateGainValue(app,app.Gain7EditField,app.Gain7Slider);
            app.Gain7EditField.ValueChangedFcn = @(~,~) updateGainSlider(app,app.Gain7Slider,app.Gain7EditField);

            % Create Gain8Slider
            app.Gain8Slider = uislider(app.UIFigure);
            app.Gain8Slider.Limits = [-12 12];
            app.Gain8Slider.MajorTicks = [-12 -9 -6 -3 0 3 6 9 12];
            app.Gain8Slider.Position = [695 425 300 3];
            app.Gain8Slider.Value = 1;
            
            % Create Gain8EditField
            app.Gain8EditField = uieditfield(app.UIFigure, 'text');
            app.Gain8EditField.Value = '1';
            app.Gain8EditField.Position = [1020 400 50 30];
            app.Gain8Slider.ValueChangedFcn = @(~,~) updateGainValue(app,app.Gain8EditField,app.Gain8Slider);
            app.Gain8EditField.ValueChangedFcn = @(~,~) updateGainSlider(app,app.Gain8Slider,app.Gain8EditField);

            % Create Gain9Slider
            app.Gain9Slider = uislider(app.UIFigure);
            app.Gain9Slider.Limits = [-12 12];
            app.Gain9Slider.MajorTicks = [-12 -9 -6 -3 0 3 6 9 12];
            app.Gain9Slider.Position = [695 375 300 3];
            app.Gain9Slider.Value = 1;
            
            % Create Gain9EditField
            app.Gain9EditField = uieditfield(app.UIFigure, 'text');
            app.Gain9EditField.Value = '1';
            app.Gain9EditField.Position = [1020 350 50 30];
            app.Gain9Slider.ValueChangedFcn = @(~,~) updateGainValue(app,app.Gain9EditField,app.Gain9Slider);
            app.Gain9EditField.ValueChangedFcn = @(~,~) updateGainSlider(app,app.Gain9Slider,app.Gain9EditField);

            % Create Gain10Slider
            app.Gain10Slider = uislider(app.UIFigure);
            app.Gain10Slider.Limits = [-12 12];
            app.Gain10Slider.MajorTicks = [-12 -9 -6 -3 0 3 6 9 12];
            app.Gain10Slider.Position = [695 325 300 3];
            app.Gain10Slider.Value = 1;
    
            % Create Gain10EditField
            app.Gain10EditField = uieditfield(app.UIFigure, 'text');
            app.Gain10EditField.Value = '1';
            app.Gain10EditField.Position = [1020 300 50 30];
            app.Gain10Slider.ValueChangedFcn = @(~,~) updateGainValue(app,app.Gain10EditField,app.Gain10Slider);
            app.Gain10EditField.ValueChangedFcn = @(~,~) updateGainSlider(app,app.Gain10Slider,app.Gain10EditField);

            % Create Gain1Label
            app.Gain1Label = uilabel(app.UIFigure);
            app.Gain1Label.HorizontalAlignment = 'right';
            app.Gain1Label.Position = [80 500 50 30];
            app.Gain1Label.Text = '30Hz';
    
            % Create Gain2Label
            app.Gain2Label = uilabel(app.UIFigure);
            app.Gain2Label.HorizontalAlignment = 'right';
            app.Gain2Label.Position = [80 450 50 30];
            app.Gain2Label.Text = '60Hz';
    
            % Create Gain3Label
            app.Gain3Label = uilabel(app.UIFigure);
            app.Gain3Label.HorizontalAlignment = 'right';
            app.Gain3Label.Position = [80 400 50 30];
            app.Gain3Label.Text = '120Hz';
    
            % Create Gain4Label
            app.Gain4Label = uilabel(app.UIFigure);
            app.Gain4Label.HorizontalAlignment = 'right';
            app.Gain4Label.Position = [80 350 50 30];
            app.Gain4Label.Text = '240Hz';
    
            % Create Gain5Label
            app.Gain5Label = uilabel(app.UIFigure);
            app.Gain5Label.HorizontalAlignment = 'right';
            app.Gain5Label.Position = [80 300 50 30];
            app.Gain5Label.Text = '480Hz';
    
            % Create EQButton
            app.EQButton = uibutton(app.UIFigure, 'push');
            app.EQButton.ButtonPushedFcn = createCallbackFcn(app, @EQButtonPushed, true);
            app.EQButton.Position = [500 225 100 30];
            app.EQButton.Text = 'Equalize Audio';
    
            % Create Gain6Label
            app.Gain6Label = uilabel(app.UIFigure);
            app.Gain6Label.HorizontalAlignment = 'right';
            app.Gain6Label.Position = [600 500 50 30];
            app.Gain6Label.Text = '960Hz';
    
            % Create Gain7Label
            app.Gain7Label = uilabel(app.UIFigure);
            app.Gain7Label.HorizontalAlignment = 'right';
            app.Gain7Label.Position = [600 450 50 30];
            app.Gain7Label.Text = '1920Hz';
    
            % Create Gain8Label
            app.Gain8Label = uilabel(app.UIFigure);
            app.Gain8Label.HorizontalAlignment = 'right';
            app.Gain8Label.Position = [600 400 50 30];
            app.Gain8Label.Text = '3840Hz';
    
            % Create Gain9Label
            app.Gain9Label = uilabel(app.UIFigure);
            app.Gain9Label.HorizontalAlignment = 'right';
            app.Gain9Label.Position = [600 350 50 30];
            app.Gain9Label.Text = '7680Hz';

            % Create Gain10Label
            app.Gain9Label = uilabel(app.UIFigure);
            app.Gain9Label.HorizontalAlignment = 'right';
            app.Gain9Label.Position = [600 300 50 30];
            app.Gain9Label.Text = '15360Hz';

            % Create Play1Button
            app.Play1Button = uibutton(app.UIFigure,'push');
            app.Play1Button.ButtonPushedFcn = createCallbackFcn(app, @Play1ButtonPushed, true);
            app.Play1Button.Position = [350 125 100 30];
            app.Play1Button.Text = 'Play 1';

            % Create Play2Button
            app.Play2Button = uibutton(app.UIFigure,'push');
            app.Play2Button.ButtonPushedFcn = createCallbackFcn(app, @Play2ButtonPushed, true);
            app.Play2Button.Position = [650 125 100 30];
            app.Play2Button.Text = 'Play 2';

            % Show the figure after all components are created
            app.UIFigure.Visible = 'on';
        end
        
        function showMessageBox(app, condition, message)
            if condition
                uialert(app.UIFigure, message, 'Information');
            end
        end

        function updateGainValue(~, EF, S)
            EF.Value = num2str(S.Value);
        end
        
        function updateGainSlider(app, S, EF)
            if isnan(str2double(EF.Value))
                showMessageBox(app, true, 'Not a number');
                EF.Value = num2str(S.Value);
            elseif str2double(EF.Value)>12
                showMessageBox(app, true, 'Over max ratio!');
                EF.Value = num2str(S.Value);
            elseif str2double(EF.Value)<-12
                showMessageBox(app, true, 'Over max ratio!');
                EF.Value = num2str(S.Value);
            else
            S.Value = str2double(EF.Value);
            end
        end

        % Button pushed function: EQButton
        function EQButtonPushed(app, ~)
            % Disable equalize button
            if app.flag1 == 0
                showMessageBox(app, true, 'Choose your audio file first!');
            else
                try
                    app.EQButton.Enable = 'off';
                    drawnow;
            
                    % Load audio file
                    [app.y, app.Fs] = audioread(app.AudioFileEdit.Value );
            
                    % Apply equalization
                    fc = [30 60 120 240 480 960 1920 3840 7680 15360];
                    gain = [app.Gain1Slider.Value, app.Gain2Slider.Value, app.Gain3Slider.Value, app.Gain4Slider.Value, app.Gain5Slider.Value, app.Gain6Slider.Value, app.Gain7Slider.Value, app.Gain8Slider.Value, app.Gain9Slider.Value, app.Gain10Slider.Value];
                    num_bands = length(fc);
            
                    app.B = cell(num_bands, 1);
                    app.A = cell(num_bands, 1);
                    for i = 1:num_bands
                        [app.B{i}, app.A{i}] = butter(2, [fc(i)*(2^(-1/6))*0.9, fc(i)*(2^(1/6))*1.1]/(app.Fs/2), 'bandpass');
                    end
            
                    app.y_eq = zeros(size(app.y));
                    for i = 1:num_bands
                        app.y_eq = app.y_eq + gain(i)*filter(app.B{i}, app.A{i}, app.y);
                    end
                    app.y_eq = app.y_eq/mean(abs(app.y_eq))*mean(abs(app.y));
                    
                    audiowrite('equalized_audio.wav', app.y_eq, app.Fs);
                    msgbox('Saved as equalized_audio.wav in your working directory.', 'Saved successfully.');
                    % Update equalized audio plot
                    plot(app.EqualizedAxes, (1:length(app.y_eq))/app.Fs, app.y_eq, 'r');
                    xlabel(app.EqualizedAxes, 'Time (s)');
                    ylabel(app.EqualizedAxes, 'Amplitude');
                    title(app.EqualizedAxes, 'Equalized Audio - Time Domain');
            
                    % Enable equalize button
                    app.EQButton.Enable = 'on';
                    drawnow;
                    app.flag2 = 1; 
                catch
                    showMessageBox(app, true, 'Bad equalization! Reset params.')
                    app.EQButton.Enable = 'on';
                end
            end
        end

        function Play1ButtonPushed(app, ~)
            if app.flag1 == 0
                showMessageBox(app, true, 'Choose your audio file first!');
            else
                if app.Play1Button.Text(1) == 'P'
                    app.player1 = audioplayer(app.y, app.Fs);
                    app.Play1Button.Text = 'Stop';
                    play(app.player1);
                else
                    app.Play1Button.Text = 'Play 1';
                    if isvalid(app.player1)
                        stop(app.player1);
                    end
                end
            end
        end

        function Play2ButtonPushed(app, ~)
            if app.flag2 == 0
                showMessageBox(app, true, 'Apply equalizer first!');
            else
                if app.Play2Button.Text(1) == 'P'
                    app.player2 = audioplayer(app.y_eq, app.Fs);
                    app.Play2Button.Text = 'Stop';
                    play(app.player2);
                else
                    app.Play2Button.Text = 'Play 2';
                    if isvalid(app.player2)
                        stop(app.player2);
                    end
                end
            end
         end

        % Delete app
        function delete(app)
            % Delete UIFigure when app is deleted
            if ~isempty(app.player1) && isplaying(app.player1)
                stop(app.player1);
                delete(app.player1);
            end
            if ~isempty(app.player2) && isplaying(app.player2)
                stop(app.player2);
                delete(app.player2);
            end
            delete(app.UIFigure)
        end
        
    end

end

    


