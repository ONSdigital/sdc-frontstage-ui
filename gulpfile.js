var gulp = require('gulp'),
	sass = require('gulp-sass'),
	concat = require('gulp-concat'),
	livereload = require('gulp-livereload'),
	mustache = require('gulp-mustache'),

	config = {
		sassSrc: './sass/*.scss',
		templatesSrc: ['./templates/**/*.mustache', './mock-pages/**/*.html'],
		outputDir: './dist'
	};


gulp.task('compile:templates', () => {
	return gulp.src('./mock-pages/src/**/*.html')
		.pipe(mustache({
			title: 'Log in to your account'
		}))
		.pipe(gulp.dest('./mock-pages/dist'));
});

gulp.task('compile:sass', () => {
	return gulp.src(config.sassSrc)
		.pipe(sass())
		//.pipe(concat('site.min.css'))
		.pipe(gulp.dest(config.outputDir))
		.pipe(livereload());
});

gulp.task('watch:templates', () => {
	gulp.watch(config.templatesSrc, ['compile:templates']);
});

gulp.task('watch:compile:sass', ['compile:sass'], () => {
	gulp.watch(config.sassSrc, ['compile:sass']);
});



gulp.task('dev', [
	'compile:sass',
	'compile:templates',
	'watch:compile:sass',
	'watch:templates'
], () => {
	livereload.listen();
});