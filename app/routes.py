from flask import render_template, request, redirect, url_for, flash, jsonify
from . import db
from .models import Landmark, VisitLog
from .forms import LandmarkForm, TouristVisitForm
from flask import Blueprint
import qrcode
import io
from flask import send_file
from PIL import Image, ImageDraw, ImageFont

main = Blueprint('main', __name__)

@main.route('/')
def index():
    landmarks = Landmark.query.all()
    return render_template('index.html', landmarks=landmarks)

@main.route('/landmark/add', methods=['POST'])
def add_landmark():
    name = request.form.get('name')
    location = request.form.get('location')
    if name and location:
        landmark = Landmark(name=name, location=location)
        db.session.add(landmark)
        db.session.commit()
        return '', 204
    return 'Invalid input', 400

@main.route('/landmark/<int:landmark_id>/qrcode')
def landmark_qrcode(landmark_id):
    return "This feature is now disabled. Please use the general QR code at /qrcode.", 410

@main.route('/landmark/<int:landmark_id>/visit', methods=['GET', 'POST'])
def log_visit(landmark_id):
    # Redirect all landmark-specific QR code scans to the general visit form, pre-selecting the landmark
    return redirect(url_for('main.general_visit', landmark_id=landmark_id))

@main.route('/landmark/<int:landmark_id>/logs')
def visit_logs(landmark_id):
    landmark = Landmark.query.get_or_404(landmark_id)
    visits = VisitLog.query.filter_by(landmark_id=landmark_id).order_by(VisitLog.timestamp.desc()).all()
    return render_template('visit_logs.html', landmark=landmark, visits=visits)

@main.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@main.route('/api/landmarks')
def api_landmarks():
    landmarks = Landmark.query.all()
    data = [
        {
            'id': l.id,
            'name': l.name,
            'location': l.location
        } for l in landmarks
    ]
    return jsonify(data)

@main.route('/api/visits')
def api_visits():
    visits = VisitLog.query.all()
    data = [
        {
            'id': v.id,
            'landmark_id': v.landmark_id,
            'timestamp': v.timestamp.isoformat(),
            'tourist_info': v.tourist_info
        } for v in visits
    ]
    return jsonify(data)

@main.route('/visit', methods=['GET', 'POST'])
def general_visit():
    form = TouristVisitForm()
    landmarks = Landmark.query.all()
    selected_landmark_id = request.args.get('landmark_id', type=int)
    if request.method == 'POST':
        landmark_id = request.form.get('landmark_id', type=int)
        gps_lat = request.form.get('gps_lat')
        gps_lng = request.form.get('gps_lng')
        tourist_count = request.form.get('tourist_count', type=int)
        info = f"Name: {form.name.data}, Email: {form.email.data}, Nationality: {form.nationality.data}, GPS: {gps_lat},{gps_lng}, Count: {tourist_count}"
        visit = VisitLog(landmark_id=landmark_id, tourist_info=info)
        db.session.add(visit)
        db.session.commit()
        return '', 204  # No redirect, just success for AJAX
    return render_template('visit_form.html', form=form, landmarks=landmarks, selected_landmark_id=selected_landmark_id)

@main.route('/landmarks', methods=['GET'])
def list_landmarks():
    landmarks = Landmark.query.all()
    return render_template('admin_dashboard.html', landmarks=landmarks)

@main.route('/landmark/<int:landmark_id>', methods=['GET'])
def get_landmark(landmark_id):
    landmark = Landmark.query.get_or_404(landmark_id)
    return jsonify({
        'id': landmark.id,
        'name': landmark.name,
        'location': landmark.location
    })

@main.route('/landmark/<int:landmark_id>/edit', methods=['POST'])
def edit_landmark(landmark_id):
    landmark = Landmark.query.get_or_404(landmark_id)
    name = request.form.get('name')
    location = request.form.get('location')
    if name:
        landmark.name = name
    if location:
        landmark.location = location
    db.session.commit()
    return '', 204

@main.route('/landmark/<int:landmark_id>/delete', methods=['POST'])
def delete_landmark(landmark_id):
    landmark = Landmark.query.get_or_404(landmark_id)
    db.session.delete(landmark)
    db.session.commit()
    return '', 204

@main.route('/qrcode')
def general_qrcode():
    # QR code points to the general visit form
    qr_url = url_for('main.general_visit', _external=True)
    img = qrcode.make(qr_url)
    # Add label on top
    label = "Lipa City Tourist Check-in"
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    font_size = 18
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    try:
        bbox = draw.textbbox((0, 0), label, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = font.getsize(label)
    new_img = Image.new('RGB', (img.width, img.height + text_height + 10), 'white')
    new_img.paste(img, (0, text_height + 10))
    draw = ImageDraw.Draw(new_img)
    draw.text(((img.width - text_width) // 2, 5), label, fill='black', font=font)
    buf = io.BytesIO()
    new_img.save(buf, format='PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png', as_attachment=True, download_name="lipa_city_tourist_qrcode.png")

def register_routes(app):
    app.register_blueprint(main)

# More routes for QR scan, visit logging, etc. can be added here
