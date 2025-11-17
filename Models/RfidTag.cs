using System.ComponentModel.DataAnnotations;

namespace NagyprojektBackend.Models
{
    public class RfidTag
    {
        [Key]
        public int Id { get; set; }
        public string TagId { get; set; } = null!;
        public string? Owner { get; set; }
        public bool Active { get; set; } = true;
    }
}
