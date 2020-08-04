use strict;



# To run perl fixgff.pl input.gff >output.gff






my $tmp1 = "tmp_x1.gff";
my $tmp2 = "tmp_x2.gff";

my $default_val = 2;

open (OUTFILE, ">$tmp1") or die ("cannot open file $tmp1 to write");

while (<>){

    $_=~s/\r//;

    if ($_=~/^#/){
      print $_;
      next;
    }
    
    chomp ($_);


    my ($chr, $source, $type, $start, $end, @r) = split ("\t", $_);

    my $rank = get_rank($type); 

    $start = $start + $rank;
    my $r = join ("\t", @r);
    print OUTFILE "$chr\t$source\t$type\t$start\t$end\t$r\n";
}

close (OUTFILE);


my $cmd = "sort -k1,1 -k4,4n $tmp1 > $tmp2";
system ($cmd);

open (FILE, $tmp2) or die ("can not open file $tmp2 for reading");

while (<FILE>){
    chomp ($_);
    my ($chr, $source, $type, $start, $end, @r) = split ("\t", $_);

    my $rank = get_rank($type);

    $start = $start - $rank;
    my $r = join ("\t", @r);
    print "$chr\t$source\t$type\t$start\t$end\t$r\n";
}
close (FILE);

unlink ($tmp1);
unlink ($tmp2);




sub get_rank {

  my ($type) = @_;
  $type =~s/\s*$//;
  $type =~s/^\s*//;

  my $rank = 2;

  if (uc($type) eq "GENE"){
    $rank = 0;
  }
  if (uc($type) eq "MRNA"){
    $rank = 1;
  }

  return ($rank);

}


