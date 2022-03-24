<!-- VIDEO DOM by Mark Nash and Mike Escalante -->
<!-- 1/23/22 6:15PM --> 
<link href="/wp-content/special/video-dom/style.css" type="text/css" rel="stylesheet">
<link href="/wp-content/special/video-dom/animate.css" type="text/css" rel="stylesheet">

<script src="http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
<script src="/wp-content/special/video-dom/wow.min.js"></script>
<script>
  new WOW().init();
</script>
<style>
@media (min-width: 768px) {

.artivle-video {
    width: 100%;
    height: 100%;
    object-fit: fill;
}
}
img{
  max-width: 90vw;
  max-height: 67vw;
}
  </style>

<div class="zone">
  <section class="zone-header">


    <a href="/" class="do-logo zone-menu-item"><span style="color:#FFFFFF;">DO</span></a>
    <a name = "top"/>
	<a href="#top" class="zone-title zone-menu-item"><span class="hideable" style="color:#FFFFFF;"></span> <span style="color:#FFFFFF;">THE DAILY ORANGE</span></a>

  </section>

  <? $headline = explode(": ", get_the_title()); ?>
  <div class="article-main-photo">
    <div class="article-photo">

      <video class="artivle-video" src="<?php echo get_field('videourl');?>" loop="loop" autoplay="autoplay" muted="">

      </video>
    </div>

    <hgroup class="headline-group">

      <?= get_edit_link() ?>

      <h1 style="margin-bottom: 0px;" class="wow fadeInDown"><span><? echo get_field('headline'); ?></span></h1>
      <h2 style="padding: 10px 50px; font-size: 2em; color: #fff; margin-bottom: 130px; text-align: right;font-style: italic; font-family: FloodStd;"><?php echo get_field('subheadline');?></h2>

    </hgroup> <!-- /.headline-group -->

  </div>



  <div id="post-<?php the_ID(); ?>" class="article-content article-<?= $custom_value ?>">

    <? if ( $custom_value !== 'front' ): ?>

    <article>

      <div class="article-meta">
        <?php
        $writer = $story->writers[0];
        if ($writer->writer_image){
          $writer->image_path = get_post_info($writer->writer_image);
          echo '<div class="writer-photo"><img src="'.get_resized_image('/wp-content/uploads/'.$writer->image_path->_wp_attached_file, 300, 300).'" alt="'.$writer->writer_tag.'"/></div>';
        }

        if (isset($story->writers) && count($story->writers) > 0) {
          echo '<div class="meta-byline source">By ';
          $bylines = array();
          foreach($story->writers as $writer){
            $bylines[] = '<a href="'.$writer->link.'" class="writer-name">'.$writer->name.'</a>';
          }

          echo implode(', ', $bylines);
          if (count($story->writers) == 1){

            // Check the title to see if any custom dated titles were added
            $writer_title = $story->writers[0]->writer_title;
            $titles = get_field('writer_titles', 'writers_' . $story->writers[0]->term_id);

            $time = get_the_time('U');

            if (is_object($titles)) {
              foreach ($titles as $title) {
                if (strtotime($title['start_date']) < $time && strtotime($title['end_date']) > $time) {
                  $writer_title = $title['title'];
                }
              }
            }

            if ($story->article_format == 'column' && $writer->writer_tag) {
              echo '<span class="writer-title writer-tag">' . $writer->writer_tag . '</span>';
            } else {
              echo '<span class="writer-title">'.$writer_title.'</span>';
            }
          } else {
            echo '<span class="writer-title">The Daily Orange</span>';
          }
          echo '</div>';
        }
        ?>
        <time class="meta-date published time-ago-large" datetime="<?= $story->iso_date ?>"><a href="<?php the_time('/Y/m/d/') ?>"><?php the_time('F j, Y'); ?></a> at <?php the_time('g:i a'); ?></time>

        <? include(get_template_directory() . '/includes/share-tools.php') ?>
      </div>


      <div class="entry-content">



        <? if ( $story->post_deck ): ?>
          <p class="post-deck"><?= $story->post_deck ?></p>
        <? endif ?>

        <? the_content() ?>



        <div class="writer-meta">
          <p class="article-date">Published on <a href="<?php the_time('/Y/m/d/') ?>"><?php the_time('F j, Y'); ?></a> at <?php the_time('g:i a'); ?></p>

          <?php
            // Writer descriptions

            if (isset($story->writers) && count($story->writers) > 0 && $story->article_format != 'column') {
              if (isset($writer->description) && $writer->description) {
                echo '<p>';
                echo wpautop(make_clickable_tweet(make_clickable($writer->description)));
                echo '</p>';
              }
            }
          ?>
        </div>

        <div class="post-footer">
          <div class="article-share-mod">
            <? include(get_template_directory() . '/includes/share-tools.php') ?>
          </div>

          <section class="comments">
            <?php comments_template( '', true ); ?>
          </section>
        </div>

      </div><!-- .entry-content -->


    </article>



    <? else: ?>

      <article>
        <div class="article-meta"></div>
        <div class="entry-content">
          <? the_content() ?>



        </div>
      </article>

      <div class="zone-description">
        <div>

        </div>
      </div>


      <div class="zone-front">
        <div class="zone-posts">
          <?
            $zone_posts = get_recent_posts('tag=football-guide-2016&posts_per_page=10&order=asc');
          ?>

          <? foreach ( $zone_posts as $post ): ?>
            <a href="<?= $post->path ?>" class="zone-post wow fadeInUp">
              <img src="http://dailyorange.com/resize/800x500<?= $post->image_main->image_path ?>" alt="">
              <h2><?= $post->post_title ?></h2>
            </a>
          <? endforeach; ?>
        </div>
      </div>

    <? endif; ?>


  </div><!-- .article-subdomainter-->



  <? /*include(get_template_directory() . '/includes/article-footer.php')*/ ?>

</div>


<script>
var dataHunt = {
    labels: ["Avg. Yards Per Rush", "Avg. Yards Per Pass"],
    datasets:
    [
        {
          label: "2013",
          fillColor: "rgba(35,31,32,1)",
          strokeColor: "rgba(35,31,32,0.8)",
          highlightFill: "rgba(35,31,32,0.75)",
          highlightStroke: "rgba(35,31,32,.8)",
          data: [4.7, 5.6]
        },
        {
          label: "2014",
          fillColor: "rgba(255,242,0,1)",
          strokeColor: "rgba(255,242,0,0.8)",
          highlightFill: "rgba(255,242,0,0.75)",
          highlightStroke: "rgba(255,242,0,.8)",
          data: [6, 6.8]
        }
    ]
  };

var recruitData = [
  {
    value: "34",
    color:"#939598",
    highlight: "#C5C8CC",
    label: "3 Star Recruits"
  },
  {
    value: "2",
    color: "#404041",
    highlight: "#ADAFB2",
    label: "4 Star Recruits"
  },
  {
    value: "17",
    color: "#fff200",
    highlight: "#FFF266",
    label: "Less Than 3 Stars"
  }

  ];

  var recordData = [
    {
      value: "10",
      color: "#fff200",
      highlight: "#FFF266",
      label: "WINS"
    },
    {
      value: "15",
      color:"#939598",
      highlight: "#C5C8CC",
      label: "LOSES"
    }
  ];

  var recruitCtx = document.getElementById("chart-recruits").getContext("2d");
  var myRecruits = new Chart(recruitCtx).Doughnut(recruitData);

  var recordCtx = document.getElementById("chart-record").getContext("2d");
  var myRecords = new Chart(recordCtx).Doughnut(recordData);

  var chartAYPRCtx = document.getElementById("chart-aypr").getContext("2d");
  var chartaypr = new Chart(chartAYPRCtx).Bar(dataHunt, {
      barValueSpacing: 15, barDatasetSpacing: 5,
      scaleShowGridLines: false
    // tooltipTemplate: "<%= value %>%"
   });

  document.getElementById('chartjs-legend').innerHTML = chartaypr.generateLegend();

</script>

