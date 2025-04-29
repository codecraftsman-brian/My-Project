"""
Flask routes for the Telegram Message Scheduler web interface.
"""

import os
import json
import threading
import asyncio
from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from werkzeug.utils import secure_filename

from scheduler.utils import allowed_file

# Global variables for scheduler state
is_scheduler_running = False
scheduler_thread = None

def start_scheduler_thread(scheduler):
    """Start the scheduler in a separate thread."""
    global scheduler_thread, is_scheduler_running
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def run_scheduler_async():
        global is_scheduler_running
        try:
            is_scheduler_running = True
            await scheduler.run_scheduler()
        except Exception as e:
            print(f"Scheduler error: {str(e)}")
        finally:
            is_scheduler_running = False
    
    scheduler_thread = threading.Thread(target=lambda: loop.run_until_complete(run_scheduler_async()))
    scheduler_thread.daemon = True
    scheduler_thread.start()

def register_routes(app):
    """Register all routes for the Flask application."""
    
    @app.route('/')
    def home():
        """Render the home page."""
        return render_template('index.html', 
                              messages=app.scheduler.messages,
                              targets=app.scheduler.targets,
                              config=app.scheduler.config,
                              is_running=is_scheduler_running)
    
    @app.route('/setup', methods=['GET', 'POST'])
    def setup():
        """Handle API setup."""
        if request.method == 'POST':
            api_id = request.form.get('api_id')
            api_hash = request.form.get('api_hash')
            phone = request.form.get('phone')
            wait_min = request.form.get('wait_min')
            wait_max = request.form.get('wait_max')
            
            app.scheduler.config['api_id'] = int(api_id) if api_id else 0
            app.scheduler.config['api_hash'] = api_hash
            app.scheduler.config['phone'] = phone
            app.scheduler.config['wait_time_min'] = int(wait_min) if wait_min else 30
            app.scheduler.config['wait_time_max'] = int(wait_max) if wait_max else 60
            
            # Save config
            with open(app.config['CONFIG_FILE'], 'w') as f:
                json.dump(app.scheduler.config, f, indent=4)
                
            flash('Configuration saved successfully!', 'success')
            return redirect(url_for('home'))
        
        return render_template('setup.html', config=app.scheduler.config)
    
    @app.route('/add_message', methods=['POST'])
    def add_message():
        """Add a new message."""
        message = request.form.get('message')
        if message and message.strip():
            app.scheduler.add_message(message.strip())
            flash('Message added successfully!', 'success')
        
        return redirect(url_for('home'))
    
    @app.route('/upload_messages', methods=['POST'])
    def upload_messages():
        """Upload multiple messages from a file."""
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('home'))
            
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('home'))
            
        if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process file
            count = 0
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        app.scheduler.add_message(line)
                        count += 1
                        
            flash(f'Successfully added {count} messages!', 'success')
            return redirect(url_for('home'))
        
        flash('Invalid file type. Please upload a .txt or .csv file.', 'danger')
        return redirect(url_for('home'))
    
    @app.route('/add_target', methods=['POST'])
    def add_target():
        """Add a new target."""
        name = request.form.get('name')
        target_id = request.form.get('target_id')
        target_type = request.form.get('type')
        
        if name and target_id and target_type:
            if app.scheduler.add_target(name, target_id, target_type):
                flash('Target added successfully!', 'success')
            else:
                flash('Invalid target type', 'danger')
        else:
            flash('All fields are required', 'danger')
            
        return redirect(url_for('home'))
    
    @app.route('/upload_targets', methods=['POST'])
    def upload_targets():
        """Upload multiple targets from a file."""
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(url_for('home'))
            
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(url_for('home'))
            
        if file and allowed_file(file.filename, app.config['ALLOWED_EXTENSIONS']):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process file (expecting format: name,id,type)
            count = 0
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split(',')
                        if len(parts) >= 3:
                            name = parts[0].strip()
                            target_id = parts[1].strip()
                            target_type = parts[2].strip().lower()
                            if app.scheduler.add_target(name, target_id, target_type):
                                count += 1
                        
            flash(f'Successfully added {count} targets!', 'success')
            return redirect(url_for('home'))
        
        flash('Invalid file type. Please upload a .txt or .csv file.', 'danger')
        return redirect(url_for('home'))
    
    @app.route('/reset_cycle', methods=['POST'])
    def reset_cycle():
        """Reset the current sending cycle."""
        app.scheduler.reset_cycle()
        flash('Cycle reset successfully!', 'success')
        return redirect(url_for('home'))
    
    @app.route('/start_scheduler', methods=['POST'])
    def start_scheduler():
        """Start the scheduler."""
        global is_scheduler_running
        
        if is_scheduler_running:
            flash('Scheduler is already running', 'warning')
            return redirect(url_for('home'))
            
        # Check if API credentials are set
        if app.scheduler.config['api_id'] == 0 or not app.scheduler.config['api_hash'] or not app.scheduler.config['phone']:
            flash('Please set up your Telegram API credentials first', 'danger')
            return redirect(url_for('setup'))
            
        # Check if we have messages and targets
        if not app.scheduler.messages:
            flash('Please add some messages first', 'danger')
            return redirect(url_for('home'))
            
        if not app.scheduler.targets:
            flash('Please add some targets first', 'danger')
            return redirect(url_for('home'))
        
        # Start the scheduler in a separate thread
        start_scheduler_thread(app.scheduler)
        flash('Scheduler started!', 'success')
        return redirect(url_for('home'))
    
    @app.route('/stop_scheduler', methods=['POST'])
    def stop_scheduler():
        """Stop the scheduler."""
        global scheduler_thread, is_scheduler_running
        
        if is_scheduler_running and scheduler_thread:
            # Signal the scheduler to stop
            app.scheduler.continue_running = False
            is_scheduler_running = False
            flash('Scheduler is stopping. This may take a moment.', 'warning')
        else:
            flash('Scheduler is not running', 'warning')
            
        return redirect(url_for('home'))
    
    @app.route('/delete_message/<int:index>', methods=['POST'])
    def delete_message(index):
        """Delete a message."""
        if 0 <= index < len(app.scheduler.messages):
            del app.scheduler.messages[index]
            app.scheduler._save_messages()
            flash('Message deleted successfully!', 'success')
        else:
            flash('Invalid message index', 'danger')
            
        return redirect(url_for('home'))
    
    @app.route('/delete_target/<int:index>', methods=['POST'])
    def delete_target(index):
        """Delete a target."""
        if 0 <= index < len(app.scheduler.targets):
            del app.scheduler.targets[index]
            app.scheduler._save_messages()
            flash('Target deleted successfully!', 'success')
        else:
            flash('Invalid target index', 'danger')
            
        return redirect(url_for('home'))
    
    @app.route('/auth_code', methods=['POST'])
    def set_auth_code():
        """Set the authentication code for Telegram login."""
        auth_code = request.form.get('auth_code')
        if auth_code:
            app.scheduler.auth_code = auth_code
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'No code provided'}), 400
    
    @app.route('/auth_password', methods=['POST'])
    def set_auth_password():
        """Set the 2FA password for Telegram login."""
        auth_password = request.form.get('auth_password')
        if auth_password:
            app.scheduler.auth_password = auth_password
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'No password provided'}), 400