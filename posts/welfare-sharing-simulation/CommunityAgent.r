# to show the benefits of welfare


# Example: Poisson model- each person gets 0, 1, 2, ... units of 'stuff'
#   Want strategy to minimise probability of getting 0 units of 'stuff'
#   On average, people get two pieces of 'stuff'


# 1) generate 150 individual draws of poisson(2)
ind.draws <- rpois(150, 2)



nearest.neighbour.redistribute <- function(original){

  sorter <- function(trio){
    left <- trio[1]
    mid <- trio[2]
    r <- trio[3]
     max.neighbour <- max(left, r)
    if (mid < max.neighbour)
    {
      # left > r
      if (left > r) {
        mid <- mid + 1
        left <- left -1
        } else{
          if (r > left) {
          mid <- mid + 1
          r <- r -1
        }
            else    # both equal
            {
              if (rnorm(1) > 0){           # choose a side with equal probability
                mid <- mid + 1
                left <- left - 1
              }
            else{
              mid <- mid + 1
              r <- r -1
            }
         }

        }

          }
    new.trio <- c(left, mid, r)
    return(new.trio)
  }

  #first
  trio <- original[c(length(original), 1,2)]
  new.trio <- sorter(trio)
  new.trio -> original[c(length(original), 1,2)]

  for (i in 2:(length(original)-1))
  {
    trio <- original[c(i-1, i,i+1)]
    new.trio <- sorter(trio)
    new.trio -> original[c(i-1, i,i+1)]

  }

  #last

  trio <- original[c(length(original) -1, length(original), 1)]
  new.trio <- sorter(trio)
  new.trio -> original[c(length(original) -1, length(original), 1)]



  return(original)
}

shared.draws <- nearest.neighbour.redistribute(ind.draws)

writeClipboard(as.character(ind.draws))    # for sending to excel
writeClipboard(as.character(shared.draws)) # for sending to excel

library(lattice)


matrix(nrow=2, ncol=7) -> comparison   # for putting results into
colnames(comparison) <- 0:6
rownames(comparison) <- c("Individualism", "Sharing")

comparison[1,] <- as.numeric(table(ind.draws))
comparison[2,] <- as.numeric(table(shared.draws))

comparison[2,1:5] <- as.numeric(table(shared.draws))   # only 1st 5 values occupied
comparison[2,6:7] <- 0      #filler
comparison

barplot(comparison, beside=T, legend.text=rownames(comparison), xlab="number of resources",
  ylab="Frequency", main="Effect of sharing on resource distribution")



  # part 2: spatial drought
  
ind.spat <- c( rpois(80, 3), rep(0,50), rpois(20,3))
share.spat <- nearest.neighbour.redistribute(ind.spat)

writeClipboard(as.character(ind.spat))    # for sending to excel
writeClipboard(as.character(share.spat)) # for sending to excel

N <- max(ind.spat)


matrix(nrow=2, ncol=N+1) -> comparison   # for putting results into
colnames(comparison) <- 0:N
rownames(comparison) <- c("Individualism", "Sharing")

comparison[1,] <- as.numeric(table(ind.spat))

share.tab <- rep(0,N+1)
share.tab[1:length(table(share.spat))] <- as.numeric(table(share.spat))

comparison[2,] <- share.tab
comparison

barplot(comparison, beside=T, legend.text=rownames(comparison), xlab="number of resources",
  ylab="Frequency", main="Effect of sharing on resource distribution\n(Spatial Drought)")


  # part 3a: lambda=1.5

ind.1.5 <- rpois(150, 1.5)
share.1.5 <- nearest.neighbour.redistribute(ind.1.5)

writeClipboard(as.character(ind.1.5))    # for sending to excel
writeClipboard(as.character(share.1.5)) # for sending to excel

  # part 3b: lambda=1.0

ind.1.5 <- rpois(150, 1.0)
share.1.5 <- nearest.neighbour.redistribute(ind.1.5)

writeClipboard(as.character(ind.1.5))    # for sending to excel
writeClipboard(as.character(share.1.5)) # for sending to excel


  # part 3c: lambda=.5

ind.1.5 <- rpois(150, 0.5)
share.1.5 <- nearest.neighbour.redistribute(ind.1.5)

writeClipboard(as.character(ind.1.5))    # for sending to excel
writeClipboard(as.character(share.1.5)) # for sending to excel
