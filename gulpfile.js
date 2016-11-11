var gulp = require('gulp'),
	sass = require('gulp-sass'),
	concat = require('gulp-concat'),
	mustache = require('gulp-mustache'),
	webserver = require('gulp-webserver'),
	argv = require('yargs').argv,

	fs = require('fs'),

	config = {
		sassSrc: './sass/*.scss',
		templatesSrc: [
			'./mock-pages/**/*.json',
			'./templates/**/*.mustache',
			'./mock-pages/**/*.html'
		],
		outputDir: './dist',
		templatesArr: fs.readdirSync('./mock-pages/src')
	};

var portNumber = process.env.PORT || argv.port || 8080;

config.templatesArr.forEach(file => {

	var page = file.replace('.html', '');

	gulp.task('compile:templates:' + page, () => {
		return gulp.src('./mock-pages/src/' + file)
			.pipe(mustache('./mock-pages/fixtures/' + page + '.json'))
			.pipe(gulp.dest('./mock-pages/dist'));

	});
});

gulp.task('compile:sass', () => {
	return gulp.src(config.sassSrc)
		.pipe(sass())
		.pipe(concat('site.min.css'))
		.pipe(gulp.dest(config.outputDir))
});

var templateTasks = config.templatesArr.map(page => 'compile:templates:' + page.replace('.html', ''));

gulp.task('watch:templates', templateTasks, () => {
	gulp.watch(config.templatesSrc, templateTasks);
});

gulp.task('watch:compile:sass', ['compile:sass'], () => {
	gulp.watch(config.sassSrc, ['compile:sass']);
});

gulp.task('webserver', () => {
	console.log('Using port:' + portNumber);

	gulp.src('./mock-pages/dist/')
		.pipe(webserver({
			//livereload: true,
			//directoryListing: true,
			//open: true,
			host: (process.env.NODE_ENV === 'production' ? '0.0.0.0' : 'localhost'),
			port: portNumber
		}));
});


gulp.task('test', [
	'webserver'
], () => {

});

gulp.task('dev', [
	'compile:sass',
	'watch:compile:sass',
	'watch:templates',
	'webserver'
], () => {

});