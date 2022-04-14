var url = Flask.url_for('view_participating_auctions', {user_id:getUserId()});
window.location.replace(url);
