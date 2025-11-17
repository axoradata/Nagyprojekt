using System;
using System.ComponentModel.DataAnnotations;

namespace NagyprojektBackend.Models
{
    public class LogEntry
    {
        [Key]
        public int Id { get; set; }
        public DateTime Timestamp { get; set; }
        public string Message { get; set; } = null!;
        public string? Source { get; set; }
        public int? UserId { get; set; }
    }
}
