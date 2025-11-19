using Microsoft.EntityFrameworkCore;
using NagyprojektBackend.Models;

namespace NagyprojektBackend.Data
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> opts) : base(opts) { }

        public DbSet<User> Users => Set<User>();
        public DbSet<Group> Groups => Set<Group>();
        public DbSet<LogEntry> Logs => Set<LogEntry>();
        public DbSet<RfidTag> RfidTags => Set<RfidTag>();
    }
}
