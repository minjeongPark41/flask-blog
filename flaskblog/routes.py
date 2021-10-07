import json
from flask import render_template, url_for, flash, redirect, request, jsonify
from flaskblog import app, db
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, PostForm


@app.route("/")
def index():
	return render_template('index.html')

# 순수 데이터만 리턴해주는게 필요
@app.route("/test/api/diary")
def diaryData():
	diary = request.get_json()
	return '{"a":1}'

@app.route("/diary")
def diary():
	posts = Post.query.all()
	return render_template('diary.html', posts = posts)

@app.route("/api/diary")
def apidiary():
	posts = Post.query.all()
	print(type(posts))

	# with open(posts) as apiDiaryFile:
	# 	json.dumps(posts, apiDiaryFile, indent=4 )
	# json_str = json.dumps(posts, indent=4)

	# return json.dumps(posts)

	# json.dumps(posts, default=serialize)

	# """
	# [{"id": 13, "title" : "aaa"}, {"id": 13, "title" : "aaa"}]
	# """

	list = [post.to_dict() for post in posts]
	print(list)

	return jsonify(list)

@app.route("/api/post/new", methods=['POST']) #118번째줄
def new_post2():
	# 프론트단에서 보내는 데이터를 받는 것
	json = request.get_json(force=True) #force=True 안하고도 할 수 있는 방법 알기
	print(json)
	# print(json['title'])

	post = Post(title = json['title'], content=json['content'], user_id='min')
	db.session.add(post)
	db.session.commit()

	return 'Sucesss', 200
	
@app.route("/api/update", methods=['POST'])
def update_diary():

	json = request.get_json(force=True)
	print('json >>>> ', json)
	post = Post.query.get(int(json['id']))
	post.title = json['title']
	post.contetn = json['content']
	db.session.commit()
	
	return 'Sucesss', 200


@app.route("/api/diary/<int:post_id>")
def apidiaryint(post_id):
	posts = Post.query.get(post_id)
	print(type(posts))

	list = [posts.to_dict()]
	
	print(list)

	return jsonify(list)


@app.route("/diary-detail")
def diaryDetail():
	posts = Post.query.all()
	return render_template('diary-detail.html', posts = posts)

@app.route("/article")
def article():
	return render_template('article.html', title='Article')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Acoount created for {form.username.data}!', 'success')
		return redirect(url_for('index'))
	return render_template('register.html', title='Register', form =form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('index'))
		else:
			flash('Login unsuccessful.', 'danger')
	return render_template('login.html', title='Login', form =form)

# CRUD 기능
@app.route("/post/new", methods=['GET', 'POST'])
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title = form.title.data, content=form.content.data, user_id='min')
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('diary')) 
	return render_template('create_post.html', title='New Post', 
							form=form, legend = 'Update Post')


@app.route("/post/<int:post_id>")
def post(post_id):
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title='post.title', post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	
	form = PostForm() 
	if form.validate_on_submit():

		post.title = form.title.data 
		post.content = form.content.data
		print(post.to_dict())

		db.session.commit()
		flash('Your post has been update!', 'success')
		return redirect(url_for('post', post_id=post.id))

	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', title='Update Post', 
							form=form, legend = 'Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('diary'))
	